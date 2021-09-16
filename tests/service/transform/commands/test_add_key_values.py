import unittest

from src.service.transform.commands.add_key import AddKeyValuesConfig, AddKeyValues


class TestAddKeyValues(unittest.TestCase):

    @property
    def data(self) -> dict:
        return {
            "id": 1645687,
            "a": True,
            "b": {'a': 's', 'g': [1, 2]},
            "c": [1, 2, 3, 4],
        }

    @property
    def target_data(self) -> dict:
        return {
            "id": 1645687,
            "a": True,
            "b": {'a': 's', 'b': [1, 2]},
            "c": [1, 2, 3, 4],

        }

    def test_aggregate_keys(self):
        key_values = {
            'e': True,
            'f': 'a long word'
        }
        self.transformer_config = AddKeyValuesConfig(command_name="add-key-values", key_values=key_values)
        self.transformer = AddKeyValues(config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(self.target_data, transformed_data)


if __name__ == '__main__':
    unittest.main()
