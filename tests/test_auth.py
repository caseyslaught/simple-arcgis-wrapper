
import unittest

import simple_arcgis_wrapper
from tests import AGOL_CLIENT_ID, AGOL_CLIENT_SECRET


class TestAuth(unittest.TestCase):

    def test_client_credentials_auth_valid(self):
        client = simple_arcgis_wrapper.ArcgisApi(client_id=AGOL_CLIENT_ID, client_secret=AGOL_CLIENT_SECRET)
        self.assertIsNotNone(client)

    def test_client_credentials_auth_invalid(self):
        with self.assertRaises:
            client = simple_arcgis_wrapper.ArcgisApi(client_id='', client_secret='')

