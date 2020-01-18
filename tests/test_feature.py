import random
import unittest

import simple_arcgis_wrapper as saw
from simple_arcgis_wrapper.models import PointFeature
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # random.seed(793238)
        api = saw.ArcgisAPI(
            access_token=AGOL_ACCESS_TOKEN,
            refresh_token=AGOL_REFRESH_TOKEN,
            client_id=AGOL_CLIENT_ID,
            username=AGOL_USERNAME,
        )
        feature_service = api.services.create_feature_service(
            f"Testing Feature {random.randint(0, 99)}", "This is a test."
        )
        cls.api = api
        cls.feature_service = feature_service

    @classmethod
    def tearDownClass(cls):
        # cls.api.services.delete_feature_service(cls.feature_service.id)
        cls.api.close()

    def test_create_point_feature(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Create Feature", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        point_feature = api.services.add_point(
            lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes
        )
        self.assertIsNotNone(point_feature)
        self.assertTrue(
            api.services.delete_feature_layers([fl.id], feature_service.url)
        )

    def test_get_features(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Create Feature", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        point_feature1 = api.services.add_point(
            lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes
        )
        point_feature2 = api.services.add_point(
            lon=10.2, lat=20.2, layer_url=fl.url, attributes=attributes
        )
        point_feature3 = api.services.add_point(
            lon=10.4, lat=20.4, layer_url=fl.url, attributes=attributes
        )

        features = api.services.get_features(
            feature_service.url, fl.id, "DeviceId = 'abc123'", ["OBJECTID"]
        )
        self.assertIsNotNone(features)
        self.assertTrue(isinstance(features[0], PointFeature))
        self.assertEqual(len(features), 3)

    def test_get_features_bad_where(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Create Feature - Bad Where", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        point_feature1 = api.services.add_point(
            lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes
        )
        point_feature2 = api.services.add_point(
            lon=10.2, lat=20.2, layer_url=fl.url, attributes=attributes
        )
        point_feature3 = api.services.add_point(
            lon=10.4, lat=20.4, layer_url=fl.url, attributes=attributes
        )

        with self.assertRaises(saw.exceptions.ArcGISException):
            features = api.services.get_features(
                feature_service.url, fl.id, "asdf = 100", ["OBJECTID"]
            )

    def test_get_features_bad_out_fields(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Create Feature - Bad Out Fields", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        point_feature1 = api.services.add_point(
            lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes
        )
        point_feature2 = api.services.add_point(
            lon=10.2, lat=20.2, layer_url=fl.url, attributes=attributes
        )
        point_feature3 = api.services.add_point(
            lon=10.4, lat=20.4, layer_url=fl.url, attributes=attributes
        )

        with self.assertRaises(saw.exceptions.ArcGISException):
            features = api.services.get_features(
                feature_service.url, fl.id, "DeviceId = 'abc123'", ["asdf", "qwerty"]
            )

    def test_update_features(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Update Features", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        point_feature1 = api.services.add_point(
            lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes
        )
        point_feature2 = api.services.add_point(
            lon=10.2, lat=20.2, layer_url=fl.url, attributes=attributes
        )
        point_feature3 = api.services.add_point(
            lon=10.4, lat=20.4, layer_url=fl.url, attributes=attributes
        )

        features = api.services.get_features(
            feature_service.url, fl.id, "DeviceId = 'abc123'", ["OBJECTID"]
        )

        updates = [
            (f.id, {"Name": "Casey Jones"}, {"x": 10.1, "y": 20.1}) for f in features
        ]

        # results is a dict of objectId: success (True/False)
        results = api.services.update_features(updates, fl.id, feature_service.url)
        self.assertTrue(results[updates[0][0]])
        self.assertTrue(results[updates[1][0]])
        self.assertTrue(results[updates[2][0]])

    def test_update_features_bad_attributes(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Update Features - Bad Attributes", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        point_feature1 = api.services.add_point(
            lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes
        )
        point_feature2 = api.services.add_point(
            lon=10.2, lat=20.2, layer_url=fl.url, attributes=attributes
        )
        point_feature3 = api.services.add_point(
            lon=10.4, lat=20.4, layer_url=fl.url, attributes=attributes
        )

        features = api.services.get_features(
            feature_service.url, fl.id, "DeviceId = 'abc123'", ["OBJECTID"]
        )

        updates = [(f.id, {"asdf": "lalalala"}, None) for f in features]

        results = api.services.update_features(updates, fl.id, feature_service.url)
        self.assertFalse(results[updates[0][0]])
        self.assertFalse(results[updates[1][0]])
        self.assertFalse(results[updates[2][0]])

    def test_update_features_bad_geometry(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Update Features - Bad Geometry", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        point_feature1 = api.services.add_point(
            lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes
        )
        point_feature2 = api.services.add_point(
            lon=10.2, lat=20.2, layer_url=fl.url, attributes=attributes
        )
        point_feature3 = api.services.add_point(
            lon=10.4, lat=20.4, layer_url=fl.url, attributes=attributes
        )

        features = api.services.get_features(
            feature_service.url, fl.id, "DeviceId = 'abc123'", ["OBJECTID"]
        )

        updates = [
            (f.id, {"Name": "Casey Jones"}, {"a": 10.1, "zorp": 20.1}) for f in features
        ]

        # results is a dict of objectId: success (True/False)
        results = api.services.update_features(updates, fl.id, feature_service.url)

        self.assertIsNotNone(
            api.services.get_features(
                feature_service.url, fl.id, "DeviceId = 'abc123'", ["OBJECTID"]
            )
        )
        self.assertTrue(results[updates[0][0]])
        self.assertTrue(results[updates[1][0]])
        self.assertTrue(results[updates[2][0]])

        features = api.services.get_features(
            feature_service.url, fl.id, "DeviceId = 'abc123'", ["OBJECTID"]
        )

    @staticmethod
    def create_point_feature_layer(name, api, feature_service):

        layer_fields = saw.fields.Fields()
        layer_fields.add_field(name="Date", field=saw.fields.DateField),
        layer_fields.add_field(name="Name", field=saw.fields.StringField)
        layer_fields.add_field(name="DeviceId", field=saw.fields.StringField)

        fl = api.services.create_feature_layer(
            layer_type="point",
            name=name,
            description="My test description",
            feature_service_url=feature_service.url,
            fields=layer_fields,
            x_min=10.0,
            y_min=10.0,
            x_max=20.0,
            y_max=20.0,
            wkid=4326,
        )
        return fl
