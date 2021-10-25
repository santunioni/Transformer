from typing import Dict

import pytest

from transformer.transformers.aggregate_keys import (
    AggregateKeyValue,
    AggregateKeyValueConfig,
)


@pytest.fixture
def target_data(data) -> Dict:
    t = data.copy()
    t["emails"] = [t.pop("email_1"), t.pop("email_2"), t.pop("email_3")]
    return t


def test_aggregate_keys(data, target_data):
    keys = ["email_1", "email_2", "email_3"]
    transformer = AggregateKeyValue(
        config=AggregateKeyValueConfig(keys=keys, new_key="emails")
    )
    transformed_data, _ = transformer.transform(data, {})
    for p in (transformed_data, target_data):
        p["emails"] = set(p["emails"])
    assert target_data == transformed_data


def test_aggregate_pattern(data, target_data):
    transformer = AggregateKeyValue(
        config=AggregateKeyValueConfig(pattern="^(email_).*", new_key="emails")
    )
    transformed_data, _ = transformer.transform(data, {})
    for p in (transformed_data, target_data):
        p["emails"] = set(p["emails"])
    assert target_data == transformed_data
