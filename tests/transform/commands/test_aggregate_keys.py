import unittest

from src.transform.commands.aggregate_keys import AggregateKeyValueConfig, AggregateKeyValue


class TestAggregateKeys(unittest.TestCase):

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
            "id": 1645687, "a": True, "b": {
                'a': 's', 'g': [
                    1, 2]}, "c": [
                1, 2, 3, 4], "emails": [
                    "lala@decode.buzz", "lele@decode.buzz", "lili@decode.buzz"]}

    def test_aggregate_keys(self):
        keys = ['email_1', 'email_2', 'email_3']
        self.transformer_config = AggregateKeyValueConfig(
            command_name="aggregate-keys", keys=keys, new_key='emails')
        self.transformer = AggregateKeyValue(config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(set(self.target_data['emails']), set(
            transformed_data['emails']))
        target_data = self.target_data.copy()
        del target_data['emails']
        del transformed_data['emails']
        self.assertEqual(target_data, transformed_data)

        self.transformer_config = AggregateKeyValueConfig(
            command_name="aggregate-keys", pattern='^(email_).*', new_key='emails')
        self.transformer = AggregateKeyValue(config=self.transformer_config)
        transformed_data = self.transformer.transform(self.data, {})
        self.assertEqual(set(self.target_data['emails']), set(
            transformed_data['emails']))
        target_data = self.target_data.copy()
        del target_data['emails']
        del transformed_data['emails']
        self.assertEqual(target_data, transformed_data)


if __name__ == '__main__':
    unittest.main()
