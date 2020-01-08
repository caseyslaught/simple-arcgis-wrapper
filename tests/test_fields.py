
import unittest

import simple_arcgis_wrapper as saw


class TestFields(unittest.TestCase):

    def test_add_field(self):

        m_fields = saw.Fields()
        m_fields.add_field('First Name', saw.StringField)
        m_fields.add_field('Last Name', saw.StringField)

        self.assertEqual(len(m_fields.get_fields()), 3)
        self.assertEqual(m_fields.get_fields()[1]['name'], 'First Name')
        self.assertEqual(m_fields.get_fields()[2]['name'], 'Last Name') 


