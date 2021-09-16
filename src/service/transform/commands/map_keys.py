from typing import Union, Any, Literal

from src.service.transform.abstract import TransformerConfig, Transformer


def flatten_data(
        input_data: dict[str, Union[list, set, dict, str, int, bool, float, None]]
) -> dict[str, Union[str, int, bool, float, None]]:
    sep = "."
    obj: dict[str, Union[str, int, bool, float, None]] = {}

    def scan(input_value: Union[list, set, dict[str, Any],
                                str, int, bool, float, None], parent_key: str = ""):
        if isinstance(input_value, (list, set)):
            for index, value in enumerate(input_value):
                scan(value, parent_key + (sep if parent_key !=
                                          "" else "") + "$[" + str(index) + "]")
        elif isinstance(input_value, dict):
            for key, value in input_value.items():
                scan(value, parent_key + (sep if parent_key != "" else "") + key)
        else:
            obj[parent_key] = input_value

    scan(input_data)
    return obj


class MapKeysConfig(TransformerConfig):
    command_name: Literal["map-keys"]
    mapping: dict[str, str]
    preserve_unmapped: bool = True


class MapKeys(Transformer):

    def __init__(self, config: MapKeysConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        flat_data = flatten_data(data)
        translated_dict = {}

        for map_key, map_value in self.__config.mapping.items():

            if metadata is not None:
                for meta_key, meta_value in metadata.items():
                    map_key = map_key.replace(
                        "${" + meta_key + "}", str(meta_value))
                    map_value = map_value.replace(
                        "${" + meta_key + "}", str(meta_value))

            if map_key in flat_data:
                translated_dict[map_value] = flat_data[map_key]

        if self.__config.preserve_unmapped:
            for unmapped_key in set(
                    flat_data.keys() -
                    self.__config.mapping.keys()):
                translated_dict[unmapped_key] = flat_data[unmapped_key]

        return translated_dict
