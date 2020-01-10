import json

from .field_types import DateField, DoubleField, StringField, _ObjectIdField


class Fields:
    def __init__(self):
        self._fields = [_ObjectIdField]

    def _to_json(self):
        return json.dumps(self.fields)

    def add_field(self, name, field):
        new_field = dict(field)
        new_field["name"] = name
        new_field["alias"] = name
        self._fields.append(new_field)

    def get_fields(self):
        return self._fields
