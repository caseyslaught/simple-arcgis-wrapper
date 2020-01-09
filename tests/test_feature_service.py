
import random
import unittest

import simple_arcgis_wrapper as saw
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestFeatureService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        random.seed(652589)

    def setUp(self):
        self.api = saw.ArcgisAPI(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                                 client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)

    def tearDown(self):
        self.api.close()

    def create_feature_service(self):
        name = f'SAW-Testing-{random.randint(0, 99)}'
        description = 'This is a test.'
        return self.api.create_feature_service(name, description)


    def test_create_feature_service(self):

        feature_service = self.create_feature_service()

        self.assertIsNotNone(feature_service)
        self.assertIsNotNone(feature_service.get('item_id'))
        self.assertIsNotNone(feature_service.get('name'))
        self.assertIsNotNone(feature_service.get('url'))

        self.assertTrue(self.api.delete_feature_service(feature_service['item_id']))


    def test_get_feature_service(self):

        feature_service = self.create_feature_service()

        services = self.api.get_feature_services(feature_service['name'])
        self.assertIsNotNone(services)
        self.assertEqual(len(services), 1)

        self.assertTrue(self.api.delete_feature_service(feature_service['item_id']))


    def test_update_feature_service(self):

        feature_service = self.create_feature_service()

        self.assertTrue(self.api.update_feature_service(feature_service['item_id'], title=f'{feature_service["name"]} (Updated)'))
        
        self.assertTrue(self.api.delete_feature_service(feature_service['item_id']))

