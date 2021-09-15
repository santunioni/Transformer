from typing import Optional, Union

from src.service.transform.abstract import Transformer, TransformerConfig


class AddKeyValueConfig(TransformerConfig):
    key_to_add: str
    value_to_delete: Optional[Union[str, list, dict, int, float, bool]]


class AddKeyValue(Transformer):

    def __init__(self, config: AddKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        data[self.__config.key_to_add] = self.__config.value_to_delete
        return data
