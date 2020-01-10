import random
import unittest

import simple_arcgis_wrapper as saw
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestFeatureLayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        random.seed(3141592)
        api = saw.ArcgisAPI(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                             client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)
        feature_service = api.services.create_feature_service(f'Testing {random.randint(0, 99)}', 'This is a test.')
        cls.api = api
        cls.feature_service = feature_service

    @classmethod
    def tearDownClass(cls):
        cls.api.services.delete_feature_service(cls.feature_service.id)
        cls.api.close()

    def test_create_point_feature_layer(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service
        
        fl = TestFeatureLayer.create_point_feature_layer('Test Create Point Layer', api, feature_service)

        self.assertTrue(api.services.delete_feature_layers([fl.id], feature_service.url))

    def test_create_point(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        # create the feature layer to add points to
        fl = TestFeatureLayer.create_point_feature_layer('Test Create Point', api, feature_service)

        attributes = {
            'Date': '2020-01-01 15:30:45',
            'Name': 'John Doe',
            'Altitude': 12.5
        }

        point_feature = api.services.add_point(lon=10.0, lat=20.0, layer_url=fl.url, attributes=attributes)

        self.assertIsNotNone(point_feature)

    def test_create_points(self):
        pass

    def test_get_feature_layer(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        fl = TestFeatureLayer.create_point_feature_layer('Test Get Layer', api, feature_service)
        
        fl_id = api.services.get_feature_layer(feature_service.url, layer_id=fl.id)
        fl_name = api.services.get_feature_layer(feature_service.url, layer_id=fl.id)

        self.assertIsNotNone(fl_id)
        self.assertEqual(fl_id.id, fl.id)    
        self.assertEqual(fl_id.name, fl.name)

        self.assertIsNotNone(fl_name)
        self.assertEqual(fl_name.id, fl.id)    
        self.assertEqual(fl_name.name, fl.name)


    @staticmethod
    def create_point_feature_layer(name, api, feature_service):

        layer_fields = saw.fields.Fields()
        layer_fields.add_field(name="Date", field=saw.fields.DateField),
        layer_fields.add_field(name="Name", field=saw.fields.StringField)
        layer_fields.add_field(name="Altitude", field=saw.fields.DoubleField)

        fl = api.services.create_feature_layer(layer_type='point', name=name, description='My test description', 
                                         feature_service_url=feature_service.url, fields=layer_fields, 
                                         x_min=10.0, y_min=10.0, x_max=20.0, y_max=20.0, wkid=4326)
        return fl








