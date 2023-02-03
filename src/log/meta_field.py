#
# DeepRacer Guru
#
# Version 4.0 onwards
#
# Copyright (c) 2023 dmh23
#

import re
from enum import Enum


class MetaFieldWrongDatatype(Exception):
    def __init__(self, expected_type: type, actual_type: type, field_name: str):
        super().__init__("Expected type <{}> but received type <{}> for field {}".format(expected_type.__name__,
                                                                                         actual_type.__name__,
                                                                                         field_name))


class MetaFieldMissingMandatoryValue(Exception):
    pass


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
        assert (JSON_PATH_VALID_RE.match(json_path))
        assert (data_type in [int, float, str])
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

    def set(self, value):
        if not isinstance(value, self._data_type):
            raise MetaFieldWrongDatatype(self._data_type, type(value), self._field_name)

        if self._min_value is not None and value < self._min_value:
            raise MetaFieldNumberOutOfRange

        if self._max_value is not None and value > self._max_value:
            raise MetaFieldNumberOutOfRange

        self._value = value

    def get(self):
        return self._value

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
                parent_node[self._split_path[-1]] = self._value

    def get_from_json(self, input_json: dict):
        parent_node = input_json
        for node_name in self._split_path[:-1]:
            try:
                parent_node = parent_node[node_name]
            except KeyError:
                if self._optionality == Optionality.MANDATORY:
                    raise MetaFieldMissingMandatoryValue
                else:
                    return
        try:
            self.set(parent_node[self._split_path[-1]])
        except KeyError:
            if self._optionality == Optionality.MANDATORY:
                raise MetaFieldMissingMandatoryValue


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
