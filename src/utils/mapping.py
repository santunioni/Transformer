import itertools
from typing import Any, Tuple


def choose_map_or_reversed_map(keys: set[str], mapping: dict[str, str]) -> Tuple[set[str], dict[str, str]]:
    reversed_mapping: dict[str, str] = dict(((v, k) for k, v in mapping.items()))
    mapping_keys = set(mapping.keys())
    reversed_mapping_keys = set(reversed_mapping.keys())
    if len(keys & mapping_keys) > len(keys & reversed_mapping_keys):
        return keys & mapping_keys, mapping
    return keys & reversed_mapping_keys, reversed_mapping


def map_keys(
    data: dict[str, Any], mapping: dict[str, str], preserve_unmapped: bool = True
) -> Tuple[dict[str, Any], dict[str, Any]]:
    """
    A function which takes data and a mapping and return the mapped data. The functions also discovers the correct
    order the mapping in case the wrong order is provided.
    """
    keys_in_data = set(data.keys())

    keys_intersection, to_map = choose_map_or_reversed_map(keys=keys_in_data, mapping=mapping)

    mapped_data = filter(
        lambda kv: kv[1] is not None,
        map(lambda k: (to_map[k], data[k]), keys_intersection)
    )
    unmapped_data = filter(
        lambda kv: kv[1] is not None,
        map(lambda k: (k, data[k]), keys_in_data - keys_intersection)
    )

    if preserve_unmapped:
        return dict(itertools.chain(unmapped_data, mapped_data)), dict(unmapped_data)

    return dict(mapped_data), dict(unmapped_data)
