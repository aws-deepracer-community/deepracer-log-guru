from enum import Enum


class MetaFieldWrongDatatype(Exception):
    pass


class MetaFieldMissingMandatoryValue(Exception):
    pass


class Optionality(Enum):
    MANDATORY = 1,
    OPTIONAL = 2


class MetaField:
    def __init__(self, json_path: str, data_type: type, optionality: Optionality):
        self._json_path = json_path
        self._data_type = data_type
        self._optionality = optionality
        self._value = None

    def set(self, value):
        if not isinstance(value, self._data_type):
            raise MetaFieldWrongDatatype()
        self._value = value

    def get(self):
        return self._value

    def add_to_json(self, output_json: dict):
        if self._value is None and self._optionality == Optionality.MANDATORY:
            raise MetaFieldMissingMandatoryValue

        if self._value is not None:
            output_json[self._json_path] = self._value

    def get_from_json(self, input_json: dict):
        try:
            self.set(input_json[self._json_path])
        except KeyError:
            if self._optionality == Optionality.MANDATORY:
                raise MetaFieldMissingMandatoryValue

    @staticmethod
    def create_json(fields: list):
        output_json = {}
        for f in fields:
            f.add_to_json(output_json)
        return output_json

    @staticmethod
    def parse_json(fields: list, input_json: dict):
        for f in fields:
            f.get_from_json(input_json)
