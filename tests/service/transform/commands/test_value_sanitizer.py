import unittest
from src.service.transform.commands.value_sanitizer import ValueSanitizerConfig, ValueSanitizer


class TestValueSanitizer(unittest.TestCase):

    @property
    def data(self) -> dict:
        return {
            "id": 1645687,
            "email_1": "NOME#gmail.com",
            "email_2": "NOME#gmail.com",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4],
        }

    @property
    def target_data(self) -> dict:
        return {
            "id": 1645687,
            "email_1": "nome@decode.buzz",
            "email_2": "nome@decode.buzz",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4]
        }

    def test_aggregate_keys(self):
        self.transformer_config = ValueSanitizerConfig(command_name="value-sanitizer",
                                                       key_pattern='^(email_).*',
                                                       sub_pattern='#gmail.com',
                                                       sub_string='@decode.buzz',
                                                       string_methods=['lower'])
        self.transformer = ValueSanitizer(config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(self.target_data, transformed_data)


if __name__ == '__main__':
    unittest.main()
