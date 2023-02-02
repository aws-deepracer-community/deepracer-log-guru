import unittest

from src.log.meta_field import MetaField


class TestFileParsingWithJsonOutput(unittest.TestCase):
    def test_simple_integer_field_output(self):
        test_integer_field = MetaField("field_1", int)
        test_integer_field.set(10)
        json_result = MetaField.create_json([test_integer_field])

        self.assertEqual(test_integer_field.get(), 10)
        self.assertEqual(json_result, {"field_1": 10})

    def test_simple_integer_field_input(self):
        test_integer_field = MetaField("field_1", int)
        MetaField.parse_json([test_integer_field], {"something else": 0, "field_1": 22})

        self.assertEqual(test_integer_field.get(), 22)

    def test_multiple_field_types_output(self):
        test_integer_field = MetaField("my_int", int)
        test_float_field = MetaField("my_float", int)
        test_string_field = MetaField("my_string", int)

        test_integer_field.set(99)
        test_float_field.set(123.45)
        test_string_field.set("Hello World")

        json_result = MetaField.create_json([test_integer_field, test_float_field, test_string_field])

        self.assertEqual(test_integer_field.get(), 99)
        self.assertEqual(test_float_field.get(), 123.45)
        self.assertEqual(test_string_field.get(), "Hello World")
        self.assertEqual(json_result, {"my_int": 99, "my_float": 123.45, "my_string": "Hello World"})

    def test_multiple_similar_fields(self):
        input_fields = []
        output_fields = []
        for x in range(0, 6):
            output_field = MetaField("field" + str(x), int)
            output_field.set(x * 2)
            output_fields.append(output_field)
            input_field = MetaField("field" + str(x), int)
            input_fields.append(input_field)

        json_result = MetaField.create_json(output_fields)

        MetaField.parse_json(input_fields, json_result)

        self.assertEqual(json_result, {"field0": 0, "field1": 2, "field2": 4, "field3": 6, "field4": 8, "field5": 10})
        expected_value = 0
        for f in input_fields:
            self.assertEqual(f.get(), expected_value)
            expected_value += 2
