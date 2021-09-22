import unittest
from src.service.transform.commands.value_sanitizer import ValueSanitizerConfig, ValueSanitizer


class TestValueSanitizer(unittest.TestCase):

    def test_aggregate_keys(self):
        data = {
            "id": 1645687,
            "email_1": "NOME#gmail.com",
            "email_2": "NOME#gmail.com",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4],
        }
        target_data = {
            "id": 1645687,
            "email_1": "nome@decode.buzz",
            "email_2": "nome@decode.buzz",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4]
        }

        self.transformer_config = ValueSanitizerConfig(command_name="value-sanitizer",
                                                       key_pattern='^(email_).*',
                                                       substitution_pattern='#gmail.com',
                                                       sub_string='@decode.buzz',
                                                       string_methods=['lower'])
        self.transformer = ValueSanitizer(config=self.transformer_config)
        transformed_data = self.transformer.transform(data, {})
        self.assertEqual(target_data, transformed_data)

    def test_cpf_mask_remover(self):
        data = {
            "id": 1645687,
            "cpf": "123.456.789-01",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4],
        }
        target_data = {
            "id": 1645687,
            "cpf": "12345678901",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4],
        }
        self.transformer_config = ValueSanitizerConfig(command_name="value-sanitizer",
                                                       key_pattern='cpf',
                                                       substitution_pattern='[^0-9]')
        self.transformer = ValueSanitizer(config=self.transformer_config)
        transformed_data = self.transformer.transform(data, {})
        self.assertEqual(target_data, transformed_data)


if __name__ == '__main__':
    unittest.main()
