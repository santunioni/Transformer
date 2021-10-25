from typing import Dict

import pytest

from transformer.transformers.del_key import DeleteKeys, DeleteKeysConfig


@pytest.fixture
def target_data(data) -> Dict:
    t = data.copy()
    for key in ("email_1", "email_2", "email_3"):
        del t[key]
    return t


def test_delete_keys(data, target_data):
    transformer = DeleteKeys(
        config=DeleteKeysConfig(keys=["email_1", "email_2", "email_3"])
    )
    transformed_data, _ = transformer.transform(data, {})
    assert target_data == transformed_data


def test_delete_pattern(data, target_data):
    transformer = DeleteKeys(config=DeleteKeysConfig(pattern="^(email_).*"))
    transformed_data, _ = transformer.transform(data, {})
    assert target_data == transformed_data
