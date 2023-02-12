#
# DeepRacer Guru
#
# Version 4.0 onwards
#
# Copyright (c) 2023 dmh23
#

import re
from enum import Enum
from typing import Self


class MetaFieldUnknownEnumValue(Exception):
    def __init__(self, enum_type: type, actual_value: str, field_name: str):
        super().__init__(
            "Unknown value <{}> of enumeration type <{}> for field <{}>".format(actual_value, enum_type.__name__,
                                                                                field_name))


class MetaFieldWrongDatatype(Exception):
    def __init__(self, expected_type: type, actual_type: type, field_name: str):
        super().__init__("Expected type <{}> but received type <{}> for field <{}>".format(expected_type.__name__,
                                                                                           actual_type.__name__,
                                                                                           field_name))


class MetaFieldInvalidValue(Exception):
    def __init__(self, allowed_values: list, actual_value, field_name: str):
        super().__init__(
            "Expected one of values {} but received value <{}> for field <{}>".format(allowed_values, actual_value,
                                                                                      field_name))


class MetaFieldValueModified(Exception):
    def __init__(self, old_value, new_value, field_name: str):
        super().__init__(
            "Value <{}> was changed to <{}> for immutable field <{}>".format(old_value, new_value, field_name)
        )


class MetaFieldMissingMandatoryValue(Exception):
    def __init__(self, field_name: str):
        super().__init__(
            "Missing value for mandatory field <{}>".format(field_name)
        )


class MetaFieldDuplicate(Exception):
    pass


class MetaFieldNumberOutOfRange(Exception):
    pass


class Optionality(Enum):
    MANDATORY = 1,
    OPTIONAL = 2


JSON_PATH_VALID_RE = re.compile("^[a-zA-Z0-9_.]*$")  # Allow only letters, numbers, underscores and full stops


class MetaField:
    def __init__(self, json_path: str, data_type: type, optionality: Optionality, min_value=None, max_value=None):
        self._is_enum = data_type.__base__ is Enum

        assert (JSON_PATH_VALID_RE.match(json_path))
        assert (data_type in [int, float, str, bool, list] or self._is_enum)
        assert (optionality in [Optionality.MANDATORY, Optionality.OPTIONAL])
        assert (min_value is None or isinstance(min_value, data_type))
        assert (max_value is None or isinstance(max_value, data_type))
        assert (min_value is None or max_value is None or min_value < max_value)

        self._field_name = json_path
        self._split_path = json_path.split(".")
        self._data_type = data_type
        self._optionality = optionality
        self._min_value = min_value
        self._max_value = max_value
        self._value = None
        self._allowed_values = None
        self._is_immutable = True

    def set_allowed_values(self, allowed_values: list):
        assert (self._value is None and self._allowed_values is None and not self._is_enum)
        self._allowed_values = allowed_values

    def allow_modifications(self) -> Self:
        self._is_immutable = False
        return self

    def set(self, value):
        if not isinstance(value, self._data_type):
            raise MetaFieldWrongDatatype(self._data_type, type(value), self._field_name)

        if self._min_value is not None and value < self._min_value:
            raise MetaFieldNumberOutOfRange

        if self._max_value is not None and value > self._max_value:
            raise MetaFieldNumberOutOfRange

        if self._allowed_values is not None:
            if isinstance(value, list):
                for item in value:
                    if item not in self._allowed_values:
                        raise MetaFieldInvalidValue(self._allowed_values, item, self._field_name)
            elif value not in self._allowed_values:
                raise MetaFieldInvalidValue(self._allowed_values, value, self._field_name)

        if self._is_immutable and self._value is not None and self._value != value:
            raise MetaFieldValueModified(self._value, value, self._field_name)

        self._value = value

    def get(self):
        return self._value

    def set_enum_str(self, value: str):
        assert self._is_enum
        for e in self._data_type:
            if e.name == value:
                self.set(e)
                return
        raise MetaFieldUnknownEnumValue(self._data_type, value, self._field_name)

    def add_to_json(self, output_json: dict):
        if self._value is None and self._optionality == Optionality.MANDATORY:
            raise MetaFieldMissingMandatoryValue(self._field_name)

        if self._value is not None:
            parent_node = output_json
            for node_name in self._split_path[:-1]:
                try:
                    parent_node = parent_node[node_name]
                except KeyError:
                    parent_node[node_name] = {}
                    parent_node = parent_node[node_name]

            if self._split_path[-1] in parent_node:
                raise MetaFieldDuplicate
            else:
                if self._is_enum:
                    value = self._value.name
                else:
                    value = self._value
                parent_node[self._split_path[-1]] = value

    def get_from_json(self, input_json: dict):
        parent_node = input_json
        for node_name in self._split_path[:-1]:
            try:
                parent_node = parent_node[node_name]
            except KeyError:
                if self._optionality == Optionality.MANDATORY:
                    raise MetaFieldMissingMandatoryValue(self._field_name)
                else:
                    return
        try:
            value = parent_node[self._split_path[-1]]
            if self._is_enum:
                self.set_enum_str(value)
            else:
                self.set(value)
        except KeyError:
            if self._optionality == Optionality.MANDATORY:
                raise MetaFieldMissingMandatoryValue(self._field_name)


class MetaFields:
    @staticmethod
    def create_json(fields: list[MetaField]):
        output_json = {}
        for f in fields:
            f.add_to_json(output_json)
        return output_json

    @staticmethod
    def parse_json(fields: list[MetaField], input_json: dict):
        for f in fields:
            f.get_from_json(input_json)
