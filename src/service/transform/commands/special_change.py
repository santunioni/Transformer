from typing import Union, Optional

from src.service.transform.abstract import Transformer, TransformerConfig


class SpecialChangeKeyValueConfig(TransformerConfig):
    key_1: str
    key_2: str
    new_value: Optional[Union[str, list, dict, int, float, bool]]


class SpecialChangeKeyValue(Transformer):

    def __init__(self, config: SpecialChangeKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        data_copy = data.copy()
        try:
            value_1 = data.get(self.__config.key_1)
            value_2 = data.get(self.__config.key_2)
            del data[self.__config.key_1]
            del data[self.__config.key_2]
            new_key_1 = self.__config.key_1 + '_' + value_1.lower()
            new_key_2 = self.__config.key_2 + '_' + value_1.lower()
            data[new_key_1] = self.__config.new_value
            data[new_key_2] = value_2
        except KeyError:
            return data_copy
        finally:
            return data
