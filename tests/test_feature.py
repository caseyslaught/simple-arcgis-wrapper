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
        cls.api.services.delete_feature_service(cls.feature_service.id)
        cls.api.close()

    def test_add_point(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Add Point", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        add = api.services.add_point(
            lon=10.0, lat=20.0, attributes=attributes,
            layer_id=fl.id, feature_service_url=feature_service.url
        )
        self.assertTrue(add)

    def test_add_points(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Add Points", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p3 = {'lon': 10.0, 'lat': 20.0, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        self.assertIsNotNone(adds)
        self.assertEqual(len(adds), 3)
        for k, v in adds.items():
            self.assertTrue(v)

    def test_delete_features_object_ids(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Delete Features - Object IDs", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p3 = {'lon': 10.0, 'lat': 20.0, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)
        object_ids = list(adds.keys())

        deletes = api.services.delete_features(
            object_ids=object_ids,
            layer_id=fl.id,
            feature_service_url=feature_service.url
        )

        self.assertIsNotNone(deletes)
        self.assertEqual(len(deletes), 3)
        for k, v in deletes.items():
            self.assertTrue(v)

    def test_delete_features_where(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeature.create_point_feature_layer(
            "Test Delete Features - Where", api, feature_service
        )

        attributes = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "DeviceId": "abc123",
        }

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p3 = {'lon': 10.0, 'lat': 20.0, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        deletes = api.services.delete_features(
            where="DeviceId = 'abc123'",
            layer_id=fl.id,
            feature_service_url=feature_service.url
        )

        self.assertIsNotNone(deletes)
        self.assertEqual(len(deletes), 3)
        for k, v in deletes.items():
            self.assertTrue(v)


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

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.2, 'lat': 20.2, **attributes}
        p3 = {'lon': 10.4, 'lat': 20.4, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        features = api.services.get_features(
            where="DeviceId = 'abc123'",
            layer_id=fl.id,
            feature_service_url=feature_service.url,
            out_fields=['OBJECTID']
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

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.2, 'lat': 20.2, **attributes}
        p3 = {'lon': 10.4, 'lat': 20.4, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        with self.assertRaises(saw.exceptions.ArcGISException):
            features = api.services.get_features(
                where="asdf = 666",
                layer_id=fl.id,
                feature_service_url=feature_service.url,
                out_fields=['OBJECTID']
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

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.2, 'lat': 20.2, **attributes}
        p3 = {'lon': 10.4, 'lat': 20.4, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        with self.assertRaises(saw.exceptions.ArcGISException):
            features = api.services.get_features(
                where="DeviceId = 'abc123'",
                layer_id=fl.id,
                feature_service_url=feature_service.url,
                out_fields=['shwifty']
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

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.2, 'lat': 20.2, **attributes}
        p3 = {'lon': 10.4, 'lat': 20.4, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        features = api.services.get_features(
            where="DeviceId = 'abc123'",
            layer_id=fl.id,
            feature_service_url=feature_service.url,
            out_fields=['OBJECTID']
        )

        updates = [
            (f.id, {"Name": "Casey Jones"}, {"x": 10.1, "y": 20.1}) for f in features
        ]

        updates_res = api.services.update_features(updates, fl.id, feature_service.url)
        for k, v in updates_res.items():
            self.assertTrue(v)

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

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.2, 'lat': 20.2, **attributes}
        p3 = {'lon': 10.4, 'lat': 20.4, **attributes}

        api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        features = api.services.get_features(
            where="DeviceId = 'abc123'",
            layer_id=fl.id,
            feature_service_url=feature_service.url,
            out_fields=['OBJECTID']
        )

        updates = [(f.id, {"letsget": "shwifty"}, None) for f in features]

        updates_res = api.services.update_features(updates, fl.id, feature_service.url)
        for k, v in updates_res.items():
            self.assertFalse(v)

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

        p1 = {'lon': 10.0, 'lat': 20.0, **attributes}
        p2 = {'lon': 10.2, 'lat': 20.2, **attributes}
        p3 = {'lon': 10.4, 'lat': 20.4, **attributes}

        adds = api.services.add_points([p1, p2, p3], fl.id, feature_service.url)

        features = api.services.get_features(
            where="DeviceId = 'abc123'",
            layer_id=fl.id,
            feature_service_url=feature_service.url,
            out_fields=['OBJECTID']
        )

        updates = [
            (f.id, {"Name": "Casey Jones"}, {"a": 10.1, "zorp": 20.1}) for f in features
        ]

        # results is a dict of objectId: success (True/False)
        updates_res = api.services.update_features(updates, fl.id, feature_service.url)
        for k, v in updates_res.items():
            self.assertTrue(v)

        features = api.services.get_features(
            where="DeviceId = 'abc123'",
            layer_id=fl.id,
            feature_service_url=feature_service.url,
            out_fields=['OBJECTID']
        )

        self.assertIsNotNone(features)

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
