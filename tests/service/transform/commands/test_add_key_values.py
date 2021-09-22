import unittest

from src.service.transform.commands.add_key import AddKeyValuesConfig, AddKeyValues


class TestAddKeyValues(unittest.TestCase):

    @property
    def data(self) -> dict:
        return {
            "id": 1645687,
            "a": "A-VALUE",
            "b": "B-VALUE",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4],
        }

    @property
    def target_data(self) -> dict:
        return {
            "id": 1645687,
            "a": "A-VALUE",
            "b": "B-VALUE",
            "e": {'a': 's', 'g': [1, 2]},
            "f": [1, 2, 3, 4],
            "a_a-value": True,
            "b_b-value": "a-value_b-value",
        }

    def test_aggregate_keys(self):
        key_values = {
            'a_${a}': True,
            'b_${b}': '${a}_${b}'
        }
        self.transformer_config = AddKeyValuesConfig(
            command_name="add-key-values", key_values=key_values)
        self.transformer = AddKeyValues(config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(self.target_data, transformed_data)


if __name__ == '__main__':
    unittest.main()
