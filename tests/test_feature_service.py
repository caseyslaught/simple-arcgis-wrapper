
import random
import unittest

import simple_arcgis_wrapper as saw
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestFeatureService(unittest.TestCase):

    def test_create_feature_service(self):

        api = saw.ArcgisAPI(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                            client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)

        name = 'Testing'
        description = 'This is a test.'
        feature_service = api.create_feature_service(name, description)

        self.assertIsNotNone(feature_service)
        self.assertIsNotNone(feature_service.get('item_id'))
        self.assertIsNotNone(feature_service.get('name'))
        self.assertIsNotNone(feature_service.get('url'))

        self.assertTrue(api.delete_feature_service(feature_service['item_id']))

        api.close()


    def test_get_feature_service(self):

        api = saw.ArcgisAPI(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                                              client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)

        name = f'Testing-{random.randint(0, 99)}'
        description = 'This is a test.'
        feature_service = api.create_feature_service(name, description)

        services = api.get_feature_services(name)
        self.assertIsNotNone(services)
        self.assertEqual(len(services), 1)

        self.assertTrue(api.delete_feature_service(feature_service['item_id']))
        api.close()


    def test_update_feature_service(self):

        api = saw.ArcgisAPI(access_token=AGOL_ACCESS_TOKEN, refresh_token=AGOL_REFRESH_TOKEN, 
                            client_id=AGOL_CLIENT_ID, username=AGOL_USERNAME)

        name = f'Testing-{random.randint(0, 99)}'
        description = 'This is a test.'
        feature_service = api.create_feature_service(name, description)

        self.assertTrue(api.update_feature_service(feature_service['item_id'], title=f'{name} (Update)'))
        
        self.assertTrue(api.delete_feature_service(feature_service['item_id']))
        api.close()




