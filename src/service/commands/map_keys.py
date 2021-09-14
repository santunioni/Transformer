from typing import Union, Any

from pydantic import BaseModel

from src.service.abstractions import TransformCommand


class MapKeysConfig(BaseModel):
    mapping: dict[str, str]
    preserve_unmapped: bool = True


class MapKeys(TransformCommand):

    def __init__(self, data: dict, metadata: dict, config: MapKeysConfig):
        """"""
        super().__init__(data, metadata)
        self.__config = config

    def __flatten(self) -> dict[str, Union[str, int, bool, float, None]]:
        """

        :return:
        """
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

        scan(self.data)
        return obj

    def execute(self) -> dict:
        """

        :return:
        """
        flat_data = self.__flatten()
        translated_dict = {}

        for map_key, map_value in self.__config.mapping.items():

            if self.metadata is not None:
                for meta_key, meta_value in self.metadata.items():
                    map_key = map_key.replace("${" + meta_key + "}", str(meta_value))
                    map_value = map_value.replace("${" + meta_key + "}", str(meta_value))

            if map_key in flat_data:
                translated_dict[map_value] = flat_data[map_key]

        if self.__config.preserve_unmapped:
            for unmapped_key in set(flat_data.keys() - self.__config.mapping.keys()):
                translated_dict[unmapped_key] = flat_data[unmapped_key]

        self.data = translated_dict
        return self.data
