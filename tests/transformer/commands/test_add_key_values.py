import unittest
from typing import Any

from transformer.commands.add_key import AddKeyValues, AddKeyValuesConfig


class TestAddKeyValues(unittest.TestCase):
    @property
    def data(self) -> dict:
        return {
            "id": 1645687,
            "a": "A-VALUE",
            "b": "B-VALUE",
            "e": {"a": "s", "g": [1, 2]},
            "f": [1, 2, 3, 4],
        }

    @property
    def target_data(self) -> dict:
        return {
            "id": 1645687,
            "a": "A-VALUE",
            "b": "B-VALUE",
            "e": {"a": "s", "g": [1, 2]},
            "f": [1, 2, 3, 4],
            "a_a-value": True,
            "b_b-value": "a-value_b-value",
        }

    def test_aggregate_keys(self):
        key_values = {"a_${a}": True, "b_${b}": "${a}_${b}"}
        transformer_config = AddKeyValuesConfig(
            name="add-key-values", key_values=key_values
        )
        transformer = AddKeyValues(config=transformer_config)
        transformed_data = transformer.transform(self.data, {})
        self.assertEqual(self.target_data, transformed_data)

    def test_empiricus_dinamize_manipulation(self):
        """
        Essa teste testa a demanda que nos passaram sobre como manipular dados que vão parar no Dinamize, para
        a esteira da Empiricus.
        """
        input_data: dict[str, Any] = {
            "plan_type": "BOLSA",
            "proposal_status": "Aprovado",
        }
        target_data: dict[str, Any] = input_data | {
            "plan_type_bolsa": True,
            "proposal_status_bolsa": True,
        }
        transformer_config = AddKeyValuesConfig(
            name="add-key-values",
            key_values={
                "plan_type_${plan_type}": True,
                "proposal_status_${plan_type}": True,
            },
        )
        transformer = AddKeyValues(config=transformer_config)
        new_data = transformer.transform(input_data, {})
        self.assertEqual(new_data, target_data)


if __name__ == "__main__":
    unittest.main()
