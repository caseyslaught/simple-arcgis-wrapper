import random
import time
import unittest

import simple_arcgis_wrapper as saw
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestFeatureService(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        random.seed(652589)

    def setUp(self):
        self.api = saw.ArcgisAPI(
            access_token=AGOL_ACCESS_TOKEN,
            refresh_token=AGOL_REFRESH_TOKEN,
            client_id=AGOL_CLIENT_ID,
            username=AGOL_USERNAME,
        )

    def tearDown(self):
        self.api.close()

    def create_feature_service(self, name=None):
        service_name = name or f"SAW Testing {random.randint(0, 99)}"
        description = "This is a test."
        return self.api.services.create_feature_service(service_name, description)

    def test_create_feature_service(self):

        feature_service = self.create_feature_service()

        self.assertIsNotNone(feature_service)
        self.assertTrue(self.api.services.delete_feature_service(feature_service.id))

    def test_create_duplicate_feature_service(self):

        name = "SAW Testing Duplicate Service"
        fs1 = self.create_feature_service(name=name)

        with self.assertRaises(saw.exceptions.ArcGISException):
            fs2 = self.create_feature_service(name=name)

        self.assertTrue(self.api.services.delete_feature_service(fs1.id))

    def test_get_feature_service(self):

        feature_service = self.create_feature_service()

        service = self.api.services.get_feature_service(feature_service.name)
        self.assertIsNotNone(service)

        self.assertTrue(self.api.services.delete_feature_service(feature_service.id))

    def test_get_one_feature_service(self):
        # verify that get_feature_service returns the exact name

        name1, name_saw, name2 = "SAW 1", "SAW", "SAW 2"
        feature_service1 = self.create_feature_service(name=name1)
        feature_service_saw = self.create_feature_service(name=name_saw)
        feature_service2 = self.create_feature_service(name=name2)

        service = self.api.services.get_feature_service(name_saw)
        self.assertIsNotNone(service)
        self.assertEqual(service.id, feature_service_saw.id)
        self.assertEqual(service.name, feature_service_saw.name)
        self.assertEqual(service.name, name_saw)
        self.assertEqual(
            service.url, feature_service_saw.url
        )  # check URL encoding of return URL

        self.assertTrue(self.api.services.delete_feature_service(feature_service1.id))
        self.assertTrue(
            self.api.services.delete_feature_service(feature_service_saw.id)
        )
        self.assertTrue(self.api.services.delete_feature_service(feature_service2.id))

    def test_update_feature_service(self):

        feature_service = self.create_feature_service()

        self.assertTrue(
            self.api.services.update_feature_service(
                feature_service.id, title=f"{feature_service.name} (Updated)"
            )
        )
        self.assertTrue(self.api.services.delete_feature_service(feature_service.id))

    def test_update_and_get_feature_service(self):

        name1 = "SAW Update and Get"
        name2 = f"{name1} (Updated)"

        feature_service = self.create_feature_service(name=name1)
        self.assertTrue(
            self.api.services.update_feature_service(feature_service.id, title=name2)
        )

        # the update takes some time to take effect
        time.sleep(5)

        # when you change the title, the name will remain the same
        service = self.api.services.get_feature_service(name=name1)

        self.assertIsNotNone(service)
        self.assertEqual(service.name, name1)
        self.assertEqual(service.title, name2)

        self.assertTrue(self.api.services.delete_feature_service(service.id))
