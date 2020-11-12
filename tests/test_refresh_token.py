
import unittest

import simple_arcgis_wrapper as saw

from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_PASSWORD, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestUsernamePassword(unittest.TestCase):

    def test_refresh_token_valid(self):

        api = saw.ArcgisAPI(
            access_token=AGOL_ACCESS_TOKEN,
            refresh_token=AGOL_REFRESH_TOKEN,
            username=AGOL_USERNAME,
            client_id=AGOL_CLIENT_ID,
        )

        self.assertTrue(api.requester.is_refresh_token_active())

        api.close()

    def test_refresh_token_invalid(self):

        api = saw.ArcgisAPI(access_token="abc123", refresh_token="def456")

        self.assertFalse(api.requester.is_refresh_token_active())
        
        api.close()
