import unittest

import simple_arcgis_wrapper as saw


class TestFields(unittest.TestCase):
    def test_add_field(self):

        fields = saw.fields.Fields()
        fields.add_field("First Name", saw.fields.StringField)
        fields.add_field("Last Name", saw.fields.StringField)

        self.assertEqual(len(fields.get_fields()), 3)
        self.assertEqual(fields.get_fields()[1]["name"], "First Name")
        self.assertEqual(fields.get_fields()[2]["name"], "Last Name")
