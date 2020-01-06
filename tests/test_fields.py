
import unittest

import simple_arcgis_wrapper.fields as saw_fields
import simple_arcgis_wrapper.fields.types as field_types


class TestFields(unittest.TestCase):

    def test_add_field(self):

        m_fields = saw_fields.Fields()
        m_fields.add_field('First Name', field_types.StringField)
        m_fields.add_field('Last Name', field_types.StringField)

        self.assertEqual(len(m_fields.get_fields()), 3)
        self.assertEqual(m_fields.get_fields()[1]['name'], 'First Name')
        self.assertEqual(m_fields.get_fields()[2]['name'], 'Last Name') 






