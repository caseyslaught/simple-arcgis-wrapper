
import random
import unittest

import simple_arcgis_wrapper as saw
import simple_arcgis_wrapper.fields as saw_fields
import simple_arcgis_wrapper.fields.types as field_types
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestFeatureLayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        client = saw.ArcgisApi(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                                            client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)
        feature_service = client.create_feature_service(f'Testing-{random.randint(0, 99)}', 'This is a test.')
        cls.client = client
        cls.feature_service = feature_service


    @classmethod
    def tearDownClass(cls):
        cls.client.delete_feature_service(cls.feature_service['item_id'])
        cls.client.close()


    def test_create_point_feature_layer(self):

        client = self.__class__.client
        feature_service = self.__class__.feature_service
        
        fl = TestFeatureLayer.create_point_feature_layer('Test Create Point Layer', client, feature_service)

        self.assertTrue(client.delete_feature_layers([fl['id']], feature_service['url']))


    def test_create_point(self):

        client = self.__class__.client
        feature_service = self.__class__.feature_service

        # create the feature layer to add points to
        fl = TestFeatureLayer.create_point_feature_layer('Test Create Point', client, feature_service)

        attributes = {
            'Date': '2020-01-01 15:30:45',
            'Name': 'John Doe',
            'Altitude': 12.5
        }

        point = client.add_point(10.0, 20.0, fl['url'], attributes=attributes)

        self.assertIsNotNone(point)


    def test_create_points(self):
        pass

    
    def test_get_feature_layer(self):

        client = self.__class__.client
        feature_service = self.__class__.feature_service

        fl = TestFeatureLayer.create_point_feature_layer('Test Get Layer', client, feature_service)
        
        fl_id = client.get_feature_layer(feature_service['url'], layer_id=fl['id'])
        fl_name = client.get_feature_layer(feature_service['url'], layer_id=fl['id'])

        self.assertIsNotNone(fl_id)
        self.assertEqual(fl_id['id'], fl['id'])    
        self.assertEqual(fl_id['name'], fl['name'])

        self.assertIsNotNone(fl_name)
        self.assertEqual(fl_name['id'], fl['id'])    
        self.assertEqual(fl_name['name'], fl['name'])


    @staticmethod
    def create_point_feature_layer(name, client, feature_service):

        fields = saw_fields.Fields()
        fields.add_field(name="Date", field=field_types.DateField)
        fields.add_field(name="Name", field=field_types.StringField)
        fields.add_field(name="Altitude", field=field_types.DoubleField)

        fl = client.create_feature_layer(layer_type='point', name=name, description='My test description', 
                                         feature_service_url=feature_service['url'], fields=fields, 
                                         x_min=10.0, y_min=10.0, x_max=20.0, y_max=20.0, wkid=4326)
        return fl








