from typing import Optional, Union, Literal

from src.service.transform.abstract import Transformer, TransformerConfig


class AddKeyValueConfig(TransformerConfig):
    name: Literal["add-key-value"]
    key: str
    value: Optional[Union[str, list, dict, int, float, bool]]


class AddKeyValue(Transformer):

    def __init__(self, config: AddKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        data[self.__config.key] = self.__config.value
        return data
