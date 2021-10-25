from typing import Any, Dict

import pytest

from transformer.transformers.add_key import AddKeyValues, AddKeyValuesConfig


@pytest.fixture()
def target_data(data):
    t = data.copy()
    t.update(
        {
            "a_a-value": True,
            "b_b-value": "a-value_b-value",
        }
    )
    return t


def test_add_placeholder(data, target_data):
    key_values = {"a_${a}": True, "b_${b}": "${a}_${b}"}
    adder = AddKeyValues(config=AddKeyValuesConfig(key_values=key_values))
    transformed_data, _ = adder.transform(data, {})
    assert target_data == transformed_data


def test_empiricus_dinamize_manipulation():
    """
    Essa teste testa a demanda que nos passaram sobre como manipular dados que vão parar no Dinamize, para
    a esteira da Empiricus.
    """
    data: Dict[str, Any] = {
        "plan_type": "BOLSA",
        "proposal_status": "Aprovado",
    }
    target_data: Dict[str, Any] = {
        **data,
        "plan_type_bolsa": True,
        "proposal_status_bolsa": True,
    }
    transformer_config = AddKeyValuesConfig(
        key_values={
            "plan_type_${plan_type}": True,
            "proposal_status_${plan_type}": True,
        },
    )
    adder = AddKeyValues(config=transformer_config)
    new_data, _ = adder.transform(data, {})
    assert new_data == target_data
