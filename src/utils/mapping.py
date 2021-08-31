from typing import Any, Union, Optional


def flatten(
        input_data: dict[str, Union[list, set, dict, str, int, bool, float, None]]
) -> dict[str, Union[str, int, bool, float, None]]:
    sep = "."
    obj: dict[str, Union[str, int, bool, float, None]] = {}

    def scan(input_value: Union[list, set, dict[str, Any], str, int, bool, float, None], parent_key: str = ""):
        if isinstance(input_value, (list, set)):
            for index, value in enumerate(input_value):
                scan(value, parent_key + (sep if parent_key != "" else "") + "$[" + str(index) + "]")
        elif isinstance(input_value, dict):
            for key, value in input_value.items():
                scan(value, parent_key + (sep if parent_key != "" else "") + key)
        else:
            obj[parent_key] = input_value

    scan(input_data)
    return obj


def map_keys(
        data: dict[str, Any], /, *,
        mapping: dict[str, str],
        metadata: Optional[dict[str, Union[str, int, bool]]] = None,
        preserve_unmapped: bool = True
) -> dict[str, Union[str, int, float, bool, None]]:
    flat_data = flatten(data)
    translated_dict = {}

    for map_key, map_value in mapping.items():

        if metadata is not None:
            for meta_key, meta_value in metadata.items():
                map_key = map_key.replace("${" + meta_key + "}", str(meta_value))
                map_value = map_value.replace("${" + meta_key + "}", str(meta_value))

        if map_key in flat_data:
            translated_dict[map_value] = flat_data[map_key]

    if preserve_unmapped:
        for unmapped_key in set(flat_data.keys() - mapping.keys()):
            translated_dict[unmapped_key] = flat_data[unmapped_key]

    return translated_dict
