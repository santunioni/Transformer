from typing import Optional, Union, Literal

from src.service.transform.abstract import Transformer, TransformerConfig


class AddKeyValuesConfig(TransformerConfig):
    command_name: Literal["add-key-values"]
    key_values: dict


class AddKeyValues(Transformer):

    def __init__(self, config: AddKeyValuesConfig):
        """
        :param config:
        """
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        # TODO: Ainda falta fazer implementação
        return data
