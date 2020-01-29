
import unittest

import simple_arcgis_wrapper as saw

from tests import AGOL_PASSWORD, AGOL_USERNAME


class TestUsernamePassword(unittest.TestCase):

    def test_username_password_valid(self):

        api = saw.ArcgisAPI.fromusernamepassword(AGOL_USERNAME, AGOL_PASSWORD)

        self.assertIsNotNone(api.requester.access_token)
        self.assertIsNone(api.requester.refresh_token)
        self.assertIsNone(api.requester.client_id)

        feature_service = api.services.create_feature_service("SAW Testing Username Password", 'this is a test')

        self.assertIsNotNone(feature_service)
        self.assertTrue(api.services.delete_feature_service(feature_service.id))

        api.close()

    def test_username_password_invalid(self):

        with self.assertRaises(saw.exceptions.ArcGISException):
            arcgis = saw.ArcgisAPI.fromusernamepassword('asdf', 'lalala')

