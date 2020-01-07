
import json
import os
import requests

from .utilities.coordinates import get_decimal_degrees_to_webmerc


ARCGIS_BASE_URL = 'https://www.arcgis.com/sharing/rest'


class ArcgisApi(object):

    def __init__(self, access_token=None, refresh_token=None, client_id=None, client_secret=None, 
                 username=None, password=None, base_url=ARCGIS_BASE_URL):

        self.base_url = base_url

        # Server-based named-user login
        if access_token is not None and refresh_token is not None and \
           client_id is not None and username is not None:

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

        # Client-credentials login
        elif client_id is not None and client_secret is not None:
            # TODO: obtain access_token by sending to token/ endpoint with client details and client_credentials type
            raise NotImplementedError('Client credentials authentication scheme not yet implemented.')

        # Username/password login
        elif username is not None and password is not None:
            raise NotImplementedError('Username/password login not yet implemented.')

        else:
            raise RuntimeError('Authentication details missing.')

        self._session = requests.Session()


    # private utilities #

    def _get_esri_type(self, layer_type):
        if layer_type == 'point':
            return 'esriGeometryPoint'
        else:
            raise NotImplementedError('Non-point geometries not implemented yet')


    def _refresh_token(self):

        if self.refresh_token is None:
            return False

        refresh_url = f'{self.base_url}/oauth2/token'

        data = {
            'client_id': self.client_id,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }

        # don't use _post/_request to avoid loop
        res = self._session.request('post', refresh_url, data=data)
        processed_response = self._process_response(res)
        
        if processed_response.get('error'):
            return False
        else:
            self.access_token = processed_response['access_token']
            return True

    def _process_response(self, response):
        return response.json()

    def _request(self, method, url, params=None, data=None):

        response = self._session.request(method, url, params=params, data=data)
        processed_response = self._process_response(response)

        # handle access token expired
        if processed_response.get('error'):
            if processed_response['error']['code'] in [498, 499]:
                if self._refresh_token():
                    data['token'] = self.access_token
                    response = self._session.request(method, url, params=params, data=data)
                    processed_response = self._process_response(response)
                    
        return processed_response


    def _get(self, url, params=dict()):
        params['f'] = 'json'
        params['token'] = self.access_token
        return self._request("get", url, params=params)


    def _post(self, url, data=dict()):
        data['f'] = 'json'
        data['token'] = self.access_token
        return self._request("post", url, data=data)


    # public methods #

    def _add_feature(self, features, layer_url):
        raise NotImplementedError()
        

    def add_point(self, x, y, layer_url, attributes=None):

        if x > 180:
            raise ValueError('invalid x value')

        if y > 90:
            raise ValueError('invalid y value')

        features = [{
            'attributes': attributes,
            'geometry': {
                'x': round(x, 8), # decimal degrees
                'y': round(y, 8)
            }
        }]

        data = {
            'features': json.dumps(features)
        }

        create_feature_url = f'{layer_url}/addFeatures'
        res = self._post(create_feature_url, data)

        if not res['addResults'][0]['success']:
            raise ArcGISException(res['addResults'][0]['error']['description'])

        return {
            'id': res['addResults'][0]['objectId']
        }


    def close(self):
        self._session.close()


    def create_feature_service(self, name, description):

        create_service_url = f'{self.base_url}/content/users/{self.username}/createService'

        create_params = {
            "name": name,
            "serviceDescription": description,
            "hasStaticData": False
        }

        data = {
            'createParameters': json.dumps(create_params),
            'outputType': 'featureService'
        }

        res = self._post(create_service_url, data)

        if not res.get('success', False):
            raise ArcGISException(res['error']['message'])

        return {
            'item_id': res['itemId'],
            'name': res['name'],
            'url': res['encodedServiceURL']
        }


    def create_feature_layer(self, layer_type, name, description, feature_service_url, fields, x_min, y_min, x_max, y_max, wkid=4326):

        esri_type = self._get_esri_type(layer_type)
        create_layer_url = feature_service_url.replace('/services/', '/admin/services/') + '/addToDefinition'

        add_to_definition = {
            "layers": [
                {
                    "name": name,
                    "description": description,
                    "type": "Feature Layer",
                    "geometryType": esri_type,
                    "extent": {
                        "type": "extent",
                        "xmin": x_min, "ymin": y_min,
                        "xmax": x_max, "ymax": y_max,
                        "spatialReference": {
                            "wkid": wkid
                        }
                    },
                    "objectIdField": "OBJECTID",
                    "fields": fields.get_fields()
                }
            ]
        }

        data = {
            'addToDefinition': json.dumps(add_to_definition),
            'outputType': 'featureService',
        }

        res = self._post(create_layer_url, data)

        if not res.get('success', False):
            raise ArcGISException(res['error']['message'])
            
        layer = res['layers'][0]
        return {
            'id': layer['id'],
            'name': layer['name'],
            'url': f'{feature_service_url}/{layer["id"]}'
        }


    def delete_feature_layers(self, layer_ids, feature_service_url):

        delete_layers_url = feature_service_url.replace('/services/', '/admin/services/') + '/deleteFromDefinition'

        deleteFromDefinition = {
            "layers":  [{ 'id': str(layer_id) } for layer_id in layer_ids]
        }

        data = {
            'deleteFromDefinition': json.dumps(deleteFromDefinition),
        }

        res = self._post(delete_layers_url, data)

        if not res.get('success', False):
            raise ArcGISException(res['error']['message'])
            
        return True


    def delete_feature_service(self, item_id):

        delete_service = f'{self.base_url}/content/users/{self.username}/items/{item_id}/delete'
        res = self._post(delete_service)
        
        if not res.get('success', False):
            raise ArcGISException(res['error']['message'])
            
        return True


    def get_feature_layer(self, feature_service_url, layer_id=None, layer_name=None):
        
        res = self._get(feature_service_url)

        if res.get('error', False):
            raise ArcGISException(res['error']['message'])

        for layer in res.get('layers', []):
            if (layer_id and int(layer_id) == layer['id']) or \
               (layer_name and layer_name == layer['name']):

                return {
                    'id': layer['id'],
                    'name': layer['name'],
                    'url': f'{feature_service_url}/{layer["id"]}'
                }


    def get_feature_services(self, keyword, owner_username=None):

        service_owner = owner_username or self.username
        search_url = f'{self.base_url}/search'
        params = {
            'q': f'title: {keyword} AND owner: {service_owner} AND type: \"Feature Service\"',
        }

        res = self._get(search_url, params)

        if res.get('results'):
            return [
                {
                    'item_id': service['id'],
                    'name': service['name'],
                    'url': service['url']
                }

                for service in res['results']
            ]


    def update_feature_service(self, feature_service_id, title=None):

        update_service_url = f'{self.base_url}/content/users/{self.username}/items/{feature_service_id}/update'

        data = {
            'title': title,
            # todo: add other attributes...
        }
        
        data = {k: v for k, v in data.items() if v is not None}
        res = self._post(update_service_url, data)

        if not res.get('success', False):
            raise ArcGISException(res['error']['message'])

        return True


class ArcGISException(Exception):
    pass



