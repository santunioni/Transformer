from src.service.transform.abstract import Transformer, TransformerConfig


class DeleteKeyValueConfig(TransformerConfig):
    key_to_delete: dict[str, str]


class DeleteKeyValue(Transformer):

    def __init__(self, config: DeleteKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        del data[self.__config.key_to_delete]
        return data
