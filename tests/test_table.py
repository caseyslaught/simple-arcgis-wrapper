import random
import unittest

import simple_arcgis_wrapper as saw
from tests import AGOL_ACCESS_TOKEN, AGOL_CLIENT_ID, AGOL_REFRESH_TOKEN, AGOL_USERNAME


class TestTable(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        api = saw.ArcgisAPI(
            access_token=AGOL_ACCESS_TOKEN,
            refresh_token=AGOL_REFRESH_TOKEN,
            client_id=AGOL_CLIENT_ID,
            username=AGOL_USERNAME,
        )
        feature_service = api.services.create_feature_service(
            f"Testing {random.randint(0, 99)}", "This is a test."
        )
        cls.api = api
        cls.feature_service = feature_service

    @classmethod
    def tearDownClass(cls):
        cls.api.services.delete_feature_service(cls.feature_service.id)
        cls.api.close()

    def test_create_table(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        table = TestTable.create_table(
            name="Test Table", 
            api=api, 
            feature_service=feature_service
        )

        fl1 = TestTable.create_point_feature_layer(
            "Test Layer 1", api, feature_service
        )

        fl2 = TestTable.create_point_feature_layer(
            "Test Layer 2", api, feature_service
        )

        self.assertTrue(api.services.delete_feature_layers([fl1.id, fl2.id], feature_service.url))
        self.assertTrue(api.services.delete_tables([table.id], feature_service.url))

    
    def test_get_table(self):

        api = self.__class__.api
        feature_service = self.__class__.feature_service

        table = TestTable.create_table(
            name="Test Get Table", 
            api=api, 
            feature_service=feature_service
        )

        table_id = api.services.get_table(feature_service.url, table_id=table.id)
        table_name = api.services.get_table(feature_service.url, table_name=table.name)

        self.assertIsNotNone(table_id)
        self.assertEqual(table_id.id, table.id)
        self.assertEqual(table_name.id, table.id)
        self.assertEqual(table_id.name, table.name)
        self.assertEqual(table_name.name, table.name)

        self.assertTrue(api.services.delete_tables([table.id], feature_service.url))


    @staticmethod
    def create_point_feature_layer(name, api, feature_service):

        layer_fields = saw.fields.Fields()
        layer_fields.add_field(name="Date", field=saw.fields.DateField),
        layer_fields.add_field(name="Name", field=saw.fields.StringField)
        layer_fields.add_field(name="Altitude", field=saw.fields.DoubleField)

        fl = api.services.create_feature_layer(
            layer_type="point",
            name=name,
            description="My test description",
            feature_service_url=feature_service.url,
            fields=layer_fields,
            x_min=10.0, y_min=10.0,
            x_max=20.0, y_max=20.0,
            wkid=4326,
        )
        return fl


    @staticmethod
    def create_table(name, api, feature_service):

        table_fields = saw.fields.Fields()
        table_fields.add_field(name="Date", field=saw.fields.DateField),
        table_fields.add_field(name="Name", field=saw.fields.StringField)
        table_fields.add_field(name="Message", field=saw.fields.StringField)

        table = api.services.create_table(
            name=name,
            description="test description",
            feature_service_url=feature_service.url,
            fields=table_fields
        )

        return table


