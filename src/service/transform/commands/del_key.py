from typing import Literal

from src.service.transform.abstract import Transformer, TransformerConfig


class DeleteKeyConfig(TransformerConfig):
    name: Literal["delete-keys"]
    keys: list[str]


class DeleteKey(Transformer):

    def __init__(self, config: DeleteKeyConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        try:
            del data[self.__config.keys]
        except KeyError:
            pass
        return data
