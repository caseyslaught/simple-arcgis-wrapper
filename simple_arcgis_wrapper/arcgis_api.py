import requests

from .services_api import ServicesAPI
from .users_api import UsersAPI


class ArcgisAPI(object):

    # TODO: possibly check if tokens and client id are legit right away cause it can cause sneaky problems

    ARCGIS_BASE_URL = "https://www.arcgis.com/sharing/rest"

    def __init__(
        self,
        access_token=None,
        refresh_token=None,
        client_id=None,
        username=None,
        base_url=ARCGIS_BASE_URL,
    ):

        try:
            self.access_token = access_token or os.environ["ARCGIS_ACCESS_TOKEN"]
        except KeyError:
            raise KeyError(
                "access token not found. Pass access_token as a kwarg or set an env var ARCGIS_ACCESS_TOKEN"
            )

        try:
            self.refresh_token = refresh_token or os.environ["ARCGIS_REFRESH_TOKEN"]
        except KeyError:
            raise KeyError(
                "refresh token not found. Pass refresh_token as a kwarg or set an env var ARCGIS_REFRESH_TOKEN"
            )

        try:
            self.client_id = client_id or os.environ["ARCGIS_CLIENT_ID"]
        except KeyError:
            raise KeyError(
                "client ID not found. Pass client_id as a kwarg or set an env var ARCGIS_CLIENT_ID"
            )

        try:
            self.username = username or os.environ["ARCGIS_USERNAME"]
        except KeyError:
            raise KeyError(
                "username not found. Pass username as a kwarg or set an env var ARCGIS_USERNAME"
            )

        self.base_url = base_url
        self.requester = Requester(access_token, refresh_token, client_id, base_url)

        # register APIs
        self.services = ServicesAPI(
            base_url=base_url, requester=self.requester, username=username
        )
        # self.users = UsersAPI(self.requester)

    def close(self):
        self.requester.session.close()

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
        "docs"
        return response.json()

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
            return False
        else:
            self.access_token = processed_response["access_token"]
            return True

    def _request(self, method, url, params=None, data=None):
        "docs"

        if method not in ["get", "post"]:
            raise ValueError("unsupported HTTP method")

        response = self.session.request(method, url, params=params, data=data)
        processed_response = self._process_response(response)

        # handle access token expired
        if processed_response.get("error"):
            if processed_response["error"].get("code") in [498, 499]:
                if self._refresh_access_token():

                    if method == "get":
                        params["token"] = self.access_token
                    elif method == "post":
                        data["token"] = self.access_token

                    response = self.session.request(
                        method, url, params=params, data=data
                    )
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
