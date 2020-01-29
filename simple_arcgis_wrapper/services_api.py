"""
docs
"""

import json

from .exceptions import ArcGISException
from .models import FeatureLayer, FeatureService, PointFeature


# TODO: use layer_url or layer_id + feature_service_url?


class ServicesAPI(object):
    def __init__(self, base_url, requester, username):
        self.base_url = base_url
        self.requester = requester
        self.username = username

    def _add_feature(self, features, layer_url):
        "docs"
        raise NotImplementedError()

    def add_point(self, lon, lat, attributes, layer_id, feature_service_url):
        "docs"

        if abs(lon) > 180: # TODO: let ArcGIS reject this?
            raise ValueError("invalid x value")

        if abs(lat) > 90:
            raise ValueError("invalid y value")

        x, y = round(lon, 8), round(lat, 8)

        features = [
            {"attributes": attributes, "geometry": {"x": x, "y": y},}  # decimal degrees
        ]

        data = {"features": json.dumps(features)}

        add_features_url = f"{feature_service_url}/{layer_id}/addFeatures"
        res = self.requester.POST(add_features_url, data)

        if res.get("error", False):
            raise ArcGISException(res["error"].get("message", "add_point error"))

        if not res["addResults"][0]["success"]:
            raise ArcGISException(res["addResults"][0]["error"]["description"])

        #return PointFeature(res["addResults"][0]["objectId"], x, y)
        return res['addResults'][0]['success']

    def add_points(self, points, layer_id, feature_service_url):
        "points is a list of dicts. Each dict must contain lon, lat and any required attributes."

        # TODO: convert Decimal to str %0.2f?

        features = list()
        for point in points:
            try:
                lon = point.pop('lon')
                lat = point.pop('lat')
            except KeyError:
                continue
            
            features.append({
                "geometry" : {"x" : lon, "y" : lat}, 
                "attributes" : {**point}
            })
        
        data = {
            'features': json.dumps(features)
        }

        add_features_url = f"{feature_service_url}/{layer_id}/addFeatures"
        res = self.requester.POST(add_features_url, data)

        if res.get("error", False):
            raise ArcGISException(res["error"].get("message", "add_points error"))

        return {u["objectId"]: u["success"] for u in res.get("addResults", [])}

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

        service = FeatureService(
            res["itemId"], res["name"], res["name"], res["encodedServiceURL"]
        )
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

    def delete_features(self, layer_id, feature_service_url, object_ids=None, where=None):
        "docs"

        if object_ids is None and where is None:
            raise ValueError('object_ids or where required')

        data = dict()

        if object_ids is not None:
            data['objectIds'] = ', '.join([str(_id) for _id in object_ids]) # convert each id to str first

        if where is not None:
            data['where'] = where

        delete_features_url = f'{feature_service_url}/{layer_id}/deleteFeatures'
        res = self.requester.POST(delete_features_url, data)
       
        if res.get("error", False):
            raise ArcGISException(res["error"].get("message", "delete_features error"))

        return {u["objectId"]: u["success"] for u in res.get("deleteResults", [])}

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

    def get_features(self, where, layer_id, feature_service_url, out_fields=[]):
        "where is an ArcGIS formatted string. out_fields is a list of fields."

        if "OBJECTID" not in out_fields:
            out_fields.append("OBJECTID")

        params = {"where": where, "outFields": ",".join(out_fields)}

        query_url = f"{feature_service_url}/{layer_id}/query"
        res = self.requester.GET(query_url, params)

        if res.get("error", False):
            raise ArcGISException(res["error"].get("message", "get_features error"))

        features = list()
        for f in res.get("features", []):
            if res["geometryType"] == "esriGeometryPoint":
                features.append(
                    PointFeature(
                        f["attributes"]["OBJECTID"],
                        f.get("geometry", {}).get("x"),
                        f.get("geometry", {}).get("y"),
                    )
                )
            else:
                raise NotImplementedError("non-point features not yet implemented")

        return features

    def get_feature_layer(self, feature_service_url, layer_id=None, layer_name=None):
        "docs"

        res = self.requester.GET(feature_service_url)
        if res.get("error", False):
            raise ArcGISException(
                res["error"].get("message", "get_feature_layer error")
            )

        for layer in res.get("layers", []):

            # explicitly use is not None because layer_id may be 0
            if (layer_id is not None and layer_id == layer["id"]) or (
                layer_name is not None and layer_name == layer["name"]
            ):
                _id, _name, _url = (
                    layer["id"],
                    layer["name"],
                    f'{feature_service_url}/{layer["id"]}',
                )
                return FeatureLayer(_id, _name, _url)

    def get_feature_service(self, name, owner_username=None):
        "docs"

        service_owner = owner_username or self.username
        search_url = f"{self.base_url}/search"
        params = {
            "q": f'title: {name} AND owner: {service_owner} AND type: "Feature Service"',
        }

        res = self.requester.GET(search_url, params)
        if res.get("error", False):
            raise ArcGISException(
                res["error"].get("message", "get_feature_service error")
            )

        for result in res.get("results", []):
            if name == result["name"]:
                return FeatureService(
                    result["id"], result["name"], result["title"], result["url"]
                )

    def update_features(self, updates, layer_id, feature_service_url):
        """
        Batch updates features. 
        updates is a list of tuples.
        Each tuple has 3 elements: (id, attribute_dict, geometry_dict)
        If not updating attributes or geometry, pass None.
        Incorrect geometries are not validated and will clear the feature's geometry.
        """

        # create updates list by adding additional attributes or geometry key
        feature_updates = []
        for u in updates:
            _id, attributes, geometry = u

            if attributes is None and geometry is None:
                continue

            fu = {"attributes": {"OBJECTID": _id}}

            if attributes is not None:
                fu["attributes"] = {**fu["attributes"], **attributes}

            if geometry is not None:
                fu["geometry"] = geometry

            feature_updates.append(fu)

        data = {
            "features": json.dumps(feature_updates),
        }

        update_features_url = f"{feature_service_url}/{layer_id}/updateFeatures"
        res = self.requester.POST(update_features_url, data)
        return {u["objectId"]: u["success"] for u in res.get("updateResults", [])}

    def update_feature_service(self, feature_service_id, title=None):
        "There is a difference between name and title. More docs..."

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
