import random
import unittest

import simple_arcgis_wrapper as saw
from simple_arcgis_wrapper.models import PointFeature, TableRow
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestTableRow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        api = saw.ArcgisAPI(
            access_token=AGOL_ACCESS_TOKEN,
            refresh_token=AGOL_REFRESH_TOKEN,
            client_id=AGOL_CLIENT_ID,
            username=AGOL_USERNAME,
        )

        feature_service = api.services.create_feature_service(
            f"Testing Table Rows {random.randint(0, 99)}", "This is a test."
        )
        cls.api = api
        cls.feature_service = feature_service

    @classmethod
    def tearDownClass(cls):
        cls.api.services.delete_feature_service(cls.feature_service.id)
        cls.api.close()

    def test_add_rows(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        table = TestTableRow.create_table(
            "Test Add Rows", api, feature_service
        )

        a1 = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        a2 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "Jane Doe",
            "Email": "jane@example.com",
        }

        a3 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "Jim Doe",
            "Email": "jim@example.com",
        }

        adds = api.services.add_table_rows([a1, a2, a3], table.id, feature_service.url)

        self.assertIsNotNone(adds)
        self.assertEqual(len(adds), 3)
        for k, v in adds.items():
            self.assertTrue(v)

    def test_delete_rows(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        table = TestTableRow.create_table(
            "Test Delete Rows", api, feature_service
        )

        a1 = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        a2 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "Jane Doe",
            "Email": "jane@example.com",
        }

        a3 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "Jim Doe",
            "Email": "jim@example.com",
        }

        adds = api.services.add_table_rows([a1, a2, a3], table.id, feature_service.url)
        object_ids = list(adds.keys())

        deletes = api.services.delete_features(
            object_ids=object_ids,
            layer_id=table.id,
            feature_service_url=feature_service.url
        )

        self.assertIsNotNone(deletes)
        self.assertEqual(len(deletes), 3)
        for k, v in deletes.items():
            self.assertTrue(v)

    def test_get_rows(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        table = TestTableRow.create_table(
            "Test Get Rows", api, feature_service
        )

        a1 = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        a2 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        a3 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        a4 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "Jane Doe",
            "Email": "jane@example.com",
        }

        adds = api.services.add_table_rows([a1, a2, a3, a4], table.id, feature_service.url)

        rows = api.services.get_table_rows(
            where="Email = 'john@example.com'",
            table_id=table.id,
            feature_service_url=feature_service.url,
            out_fields=['OBJECTID']
        )
        self.assertIsNotNone(rows)
        self.assertTrue(isinstance(rows[0], TableRow))
        self.assertEqual(len(rows), 3)

    def test_update_rows(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        table = TestTableRow.create_table(
            "Test Update Rows", api, feature_service
        )

        a1 = {
            "Date": "2020-01-01 15:30:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        a2 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        a3 = {
            "Date": "2020-01-01 15:45:45",
            "Name": "John Doe",
            "Email": "john@example.com",
        }

        adds = api.services.add_table_rows([a1, a2, a3], table.id, feature_service.url)

        rows = api.services.get_table_rows(
            where="1=1",
            table_id=table.id,
            feature_service_url=feature_service.url,
            out_fields=['OBJECTID']
        )

        updates = [(row.id, {"Name": "Jane Doe", "Email": "jane@example.com"}) for row in rows]

        updates_res = api.services.update_table_rows(updates, table.id, feature_service.url)
        for k, v in updates_res.items():
            self.assertTrue(v)

    @staticmethod
    def create_table(name, api, feature_service):

        table_fields = saw.fields.Fields()
        table_fields.add_field(name="Date", field=saw.fields.DateField),
        table_fields.add_field(name="Name", field=saw.fields.StringField)
        table_fields.add_field(name="Email", field=saw.fields.StringField)

        table = api.services.create_table(
            name=name,
            description="testing tables",
            feature_service_url=feature_service.url,
            fields=table_fields
        )

        return table
