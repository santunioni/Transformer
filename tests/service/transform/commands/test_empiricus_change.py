import unittest

from src.service.transform.commands.empiricus_change import EmpiricusChangeKeyValueConfig, EmpiricusChangeKeyValue


class TestSpecialChange(unittest.TestCase):

    @property
    def data(self) -> dict:
        return {
            "id": 1645687,
            "plan_type": "BOLSA",
            "proposal_status": "Aprovado",
            "a": "b",
            "c": "d"
        }

    @property
    def target_data(self) -> dict:
        return {
            "id": 1645687,
            "plan_type_bolsa": True,
            "proposal_status_bolsa": "Aprovado",
            "a": "b",
            "c": "d"
        }

    def test_special_change(self):
        self.transformer_config = EmpiricusChangeKeyValueConfig(
            command_name="empiricus-change",
            key_1="plan_type",
            key_2="proposal_status",
            new_value=True)
        self.transformer = EmpiricusChangeKeyValue(
            config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(self.target_data, transformed_data)


if __name__ == '__main__':
    unittest.main()
