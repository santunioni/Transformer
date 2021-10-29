import pytest

from transformer.transformers.flatters import Flatter, Unflatter


def test_flatter_returns_flat_structure(highly_nested_data):
    flat_dict = Flatter().transform(highly_nested_data)
    assert all(type(key) is str for key in flat_dict.keys())
    assert all(
        type(value) not in (dict, list, set)
        for value in filter(bool, flat_dict.values())
    )
    # The filter(bool, flat_dict.values()) iterator excludes
    # empty dicts, lists and sets from the assertion


def test_unflatter_completely_undo_flatter(highly_nested_data):
    flatten_dict = Flatter().transform(highly_nested_data)
    unflatten_dict = Unflatter().transform(flatten_dict)
    assert highly_nested_data == unflatten_dict


@pytest.fixture
def flat():
    return {
        "item[0].subitem[0].key": "value1",
        "item[0].subitem[1].key": "value2",
        "item[1].subitem[0].key": "value3",
        "item[1].subitem[1].key": "value4",
        "item2[0].subitem[0]": "value5",
        "item2[0].subitem[1]": "value6",
        "item2[1][0].key1": "value7",
        "item2[1][1].key2": "value8",
    }


@pytest.fixture
def nested():
    return {
        "item": [
            {"subitem": [{"key": "value1"}, {"key": "value2"}]},
            {"subitem": [{"key": "value3"}, {"key": "value4"}]},
        ],
        "item2": [
            {"subitem": ["value5", "value6"]},
            [{"key1": "value7"}, {"key2": "value8"}],
        ],
    }


def test_flatter(flat, nested):
    assert Flatter().transform(nested, {})[0] == flat
    assert Flatter().transform(nested) == flat


def test_unflatter(flat, nested):
    assert Unflatter().transform(flat, {})[0] == nested
    assert Unflatter().transform(flat) == nested
