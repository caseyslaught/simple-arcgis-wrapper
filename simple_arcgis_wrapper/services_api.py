"""
docs
"""

import json

from .exceptions import ArcGISException
from .models import Feature, FeatureLayer, FeatureService


class ServicesAPI(object):
    def __init__(self, base_url, requester, username):
        self.base_url = base_url
        self.requester = requester
        self.username = username

    @classmethod
    def fromclientcredentials(cls, client_id, client_secret):
        "docs"
        # TODO: get tokens then call cls() constructor
        # call cls not ArcgisAPI constructor to support subclassing
        raise NotImplementedError(
            "Client credentials initialization not yet implemented"
        )

    def _add_feature(self, features, layer_url):
        "docs"
        raise NotImplementedError()

    def add_point(self, lon=None, lat=None, layer_url=None, attributes=None):
        "docs"

        if None in [lon, lat, layer_url, attributes]:
            raise ValueError("lon, lat, layer_url, and attributes must not be None")

        if abs(lon) > 180:
            raise ValueError("invalid x value")

        if abs(lat) > 90:
            raise ValueError("invalid y value")

        features = [
            {
                "attributes": attributes,
                "geometry": {"x": round(lon, 8), "y": round(lat, 8)},  # decimal degrees
            }
        ]

        data = {"features": json.dumps(features)}

        create_feature_url = f"{layer_url}/addFeatures"
        res = self.requester.POST(create_feature_url, data)

        if not res["addResults"][0]["success"]:
            raise ArcGISException(res["addResults"][0]["error"]["description"])

        return Feature(res["addResults"][0]["objectId"])

    def create_feature_service(self, name, description):
        "docs"

        create_service_url = (
            f"{self.base_url}/content/users/{self.username}/createService"
        )

        create_params = {
            "name": name,
            "serviceDescription": description,
            "hasStaticData": False,
        }

        data = {
            "createParameters": json.dumps(create_params),
            "outputType": "featureService",
        }

        res = self.requester.POST(create_service_url, data)

        if not res.get("success", False):
            raise ArcGISException(res["error"]["message"])

        service = FeatureService(res["itemId"], res["name"], res["encodedServiceURL"])
        return service

    def create_feature_layer(
        self,
        layer_type,
        name,
        description,
        feature_service_url,  # or pass feature service object
        fields,
        x_min=0,
        y_min=0,
        x_max=10,
        y_max=10,
        wkid=4326,
    ):
        "docs"

        esri_type = ServicesAPI.get_esri_type(layer_type)

        create_layer_url = (
            feature_service_url.replace("/services/", "/admin/services/")
            + "/addToDefinition"
        )

        add_to_definition = {
            "layers": [
                {
                    "name": name,
                    "description": description,
                    "type": "Feature Layer",
                    "geometryType": esri_type,
                    "extent": {
                        "type": "extent",
                        "xmin": x_min,
                        "ymin": y_min,
                        "xmax": x_max,
                        "ymax": y_max,
                        "spatialReference": {"wkid": wkid},
                    },
                    "objectIdField": "OBJECTID",
                    "fields": fields.get_fields(),
                }
            ]
        }

        data = {
            "addToDefinition": json.dumps(add_to_definition),
            "outputType": "featureService",
        }

        res = self.requester.POST(create_layer_url, data)

        if not res.get("success", False):
            raise ArcGISException(res["error"]["message"])

        layer_data = res["layers"][0]
        _id, _name, _url = (
            layer_data["id"],
            layer_data["name"],
            f'{feature_service_url}/{layer_data["id"]}',
        )

        layer = FeatureLayer(_id, _name, _url)
        return layer

    def delete_feature_layers(self, layer_ids, feature_service_url):
        "docs"

        delete_layers_url = (
            feature_service_url.replace("/services/", "/admin/services/")
            + "/deleteFromDefinition"
        )

        deleteFromDefinition = {
            "layers": [{"id": str(layer_id)} for layer_id in layer_ids]
        }

        data = {
            "deleteFromDefinition": json.dumps(deleteFromDefinition),
        }

        res = self.requester.POST(delete_layers_url, data)

        if not res.get("success", False):
            raise ArcGISException(res["error"]["message"])

        return True

    def delete_feature_service(self, service_id):
        "docs"

        delete_service_url = (
            f"{self.base_url}/content/users/{self.username}/items/{service_id}/delete"
        )

        res = self.requester.POST(delete_service_url)

        if not res.get("success", False):
            raise ArcGISException(res["error"]["message"])

        return True

    def get_feature_layer(self, feature_service_url, layer_id=None, layer_name=None):
        "docs"

        res = self.requester.GET(feature_service_url)

        if res.get("error", False):
            raise ArcGISException(res["error"]["message"])

        for layer in res.get("layers", []):
            if (layer_id and int(layer_id) == layer["id"]) or (
                layer_name and layer_name == layer["name"]
            ):

                _id, _name, _url = (
                    layer["id"],
                    layer["name"],
                    f'{feature_service_url}/{layer["id"]}',
                )
                return FeatureLayer(_id, _name, _url)

    def get_feature_services(self, keyword, owner_username=None):
        "docs"

        service_owner = owner_username or self.username
        search_url = f"{self.base_url}/search"
        params = {
            "q": f'title: {keyword} AND owner: {service_owner} AND type: "Feature Service"',
        }

        res = self.requester.GET(search_url, params)

        if res.get("results"):
            return [
                FeatureService(s["id"], s["name"], s["url"]) for s in res["results"]
            ]

    def update_feature_service(self, feature_service_id, title=None):
        "docs"

        update_service_url = f"{self.base_url}/content/users/{self.username}/items/{feature_service_id}/update"

        data = {
            "title": title,
            # todo: add other attributes...
        }

        data = {k: v for k, v in data.items() if v is not None}
        res = self.requester.POST(update_service_url, data)

        if not res.get("success", False):
            raise ArcGISException(res["error"]["message"])

        return True

    @staticmethod
    def get_esri_type(layer_type):
        "docs"

        if layer_type == "point":
            return "esriGeometryPoint"
        else:
            raise NotImplementedError("Non-point geometries not implemented yet")
