
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
        print(feature_service)
        cls.client = client
        cls.feature_service = feature_service


    @classmethod
    def tearDownClass(cls):
        cls.client.delete_feature_service(cls.feature_service['item_id'])


    def test_create_point_feature_layer(self):
        client = self.__class__.client
        feature_service = self.__class__.feature_service
        
        fields = saw_fields.Fields()
        fields.add_field(name="Date", field=field_types.DateField)
        fields.add_field(name="Name", field=field_types.StringField)
        fields.add_field(name="Altitude", field=field_types.DoubleField)

        fl = client.create_feature_layer(layer_type='point', name='My Point Layer', description='My amazing points', 
                                         feature_service_url=feature_service['url'], fields=fields, 
                                         x_min=10.0, y_min=10.0, x_max=20.0, y_max=20.0, wkid=4326)

        self.assertTrue(client.delete_feature_layers([fl['id']], feature_service['url']))








