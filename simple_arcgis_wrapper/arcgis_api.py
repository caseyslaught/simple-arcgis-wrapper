import inspect
import json
import os
import requests
import sys

from .exceptions import ArcGISException
from .services_api import ServicesAPI
from .users_api import UsersAPI


class ArcgisAPI(object):

    ARCGIS_BASE_URL = "https://www.arcgis.com/sharing"
    ARCGIS_REST_BASE_URL = f"{ARCGIS_BASE_URL}/rest"

    # is constructor being passed arguments from ...

    def __init__(
        self,
        access_token=None,
        refresh_token=None,
        client_id=None,
        username=None,
        base_url=ARCGIS_REST_BASE_URL,
    ):

        # option 1. use constructor argument
        # option 2. use environment variable (unless fromusernamepassword then None)
        # option 3. use None

        is_pwd_auth = inspect.stack()[1].function == 'fromusernamepassword'

        try:
            self.access_token = access_token or os.environ["ARCGIS_ACCESS_TOKEN"]
        except KeyError:
            self.access_token = None

        # if username and password, refresh_token will use envar
        try:
            self.refresh_token = refresh_token or os.environ["ARCGIS_REFRESH_TOKEN"] if not is_pwd_auth else None
        except KeyError:
            self.refresh_token = None

        try:
            self.client_id = client_id or os.environ["ARCGIS_CLIENT_ID"] if not is_pwd_auth else None
        except KeyError:
            self.client_id = None

        try:
            self.username = username or os.environ["ARCGIS_USERNAME"]
        except KeyError:
            raise KeyError(
                "username not found. Pass username as a kwarg or set an env var ARCGIS_USERNAME"
            )

        self.base_url = base_url
        self.requester = Requester(
            self.access_token, self.refresh_token, self.client_id, self.base_url
        )

        # access_token cannot be empty or None when making a request so initialize it here
        if not access_token and refresh_token:
            self.requester._refresh_access_token()

        # register APIs
        self.services = ServicesAPI(
            base_url=base_url, requester=self.requester, username=username
        )

    def close(self):
        self.requester.session.close()

    @classmethod
    def fromusernamepassword(cls, username, password, base_url=ARCGIS_BASE_URL):

        token_url = f"{base_url}/generateToken"
        payload = {
            "username": username,
            "password": password,
            "referer": "www.arcgis.com",
            "f": "json",
        }

        res = requests.post(token_url, data=payload).json()
        if "error" in res:
            raise ArcGISException(res["error"]["message"])

        # need Constructor be be aware that from password auth
        ArcgisAPI._is_password_auth = True
        return cls(access_token=res["token"], username=username)


    # TODO: add properties


class Requester(object):

    # TODO: handle "private" attributes later...

    def __init__(self, access_token, refresh_token, client_id, base_url):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.session = requests.Session()
        self.base_url = base_url

    def _process_response(self, response):
        "Return JSON"
        try:
            return response.json()
        except json.decoder.JSONDecodeException:
            raise ArcGISException("ArcGIS response error. Try again later.")

    def _refresh_access_token(self):
        "docs"
        if self.refresh_token is None:
            return False

        refresh_url = f"{self.base_url}/oauth2/token"

        data = {
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }

        # don't use __post/__request to avoid loop
        res = self.session.request("post", refresh_url, data=data)
        processed_response = self._process_response(res)

        if processed_response.get("error"):
            raise ArcGISException(processed_response["error"]["message"])

        self.access_token = processed_response["access_token"]

    def _request(self, method, url, params=None, data=None):
        "docs"

        if method not in ["get", "post"]:
            raise ValueError("unsupported HTTP method")

        response = self.session.request(method, url, params=params, data=data)

        # all responses should return 200 with optional error
        if response.status_code != 200:
            raise ArcGISException(response.text)

        processed_response = self._process_response(response)

        # handle access token expired
        if processed_response.get("error"):
            if processed_response["error"].get("code") in [498, 499]:

                self._refresh_access_token()

                if method == "get":
                    params["token"] = self.access_token
                elif method == "post":
                    data["token"] = self.access_token

                response = self.session.request(method, url, params=params, data=data)
                processed_response = self._process_response(response)

        return processed_response

    def GET(self, url, params=dict()):
        "docs"
        params["f"] = "json"
        params["token"] = self.access_token
        return self._request("get", url, params=params)

    def POST(self, url, data=dict()):
        "docs"
        data["f"] = "json"
        data["token"] = self.access_token
        return self._request("post", url, data=data)

    # __add_feature = _add_feature
