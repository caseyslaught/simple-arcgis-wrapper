
import random
import unittest

import simple_arcgis_wrapper
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestFeatureService(unittest.TestCase):

    def test_create_feature_service(self):

        client = simple_arcgis_wrapper.ArcgisApi(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                                                 client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)

        name = 'Testing'
        description = 'This is a test.'
        feature_service = client.create_feature_service(name, description)

        self.assertIsNotNone(feature_service)
        self.assertIsNotNone(feature_service.get('item_id'))
        self.assertIsNotNone(feature_service.get('name'))
        self.assertIsNotNone(feature_service.get('url'))

        self.assertTrue(client.delete_feature_service(feature_service['item_id']))

        client.close()


    def test_update_feature_service(self):

        client = simple_arcgis_wrapper.ArcgisApi(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                                                 client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)

        name = f'Testing-{random.randint(0, 99)}'
        description = 'This is a test.'
        feature_service = client.create_feature_service(name, description)

        self.assertTrue(client.update_feature_service(feature_service['item_id'], title=f'{name} (Update)'))
        self.assertTrue(client.delete_feature_service(feature_service['item_id']))

        client.close()
