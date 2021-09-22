import unittest

from src.transform.commands.del_key import DeleteKeysConfig, DeleteKeys


class TestDeleteKeys(unittest.TestCase):

    @property
    def data(self) -> dict:
        return {
            "id": 1645687,
            "a": True,
            "b": {'a': 's', 'g': [1, 2]},
            "c": [1, 2, 3, 4],
            "email_1": "lala@decode.buzz",
            "email_2": "lele@decode.buzz",
            "email_3": "lili@decode.buzz",
        }

    @property
    def target_data(self) -> dict:
        return {
            "id": 1645687,
            "a": True,
            "b": {'a': 's', 'g': [1, 2]},
            "c": [1, 2, 3, 4]
        }

    def test_delete_keys(self):
        self.transformer_config = DeleteKeysConfig(
            command_name="delete-keys", keys=['email_1', 'email_2', 'email_3'])
        self.transformer = DeleteKeys(config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(self.target_data, transformed_data)
        self.transformer_config = DeleteKeysConfig(command_name="delete-keys",
                                                   pattern='^(email_).*')
        self.transformer = DeleteKeys(config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(self.target_data, transformed_data)


if __name__ == '__main__':
    unittest.main()
