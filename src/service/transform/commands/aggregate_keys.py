from src.service.transform.abstract import Transformer, TransformerConfig


class AggregateKeyValueConfig(TransformerConfig):
    key_list: list[str]
    new_key: str


class AggregateKeyValue(Transformer):

    def __init__(self, config: AggregateKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        value_list = []
        for key in self.__config.key_list:
            value_list.append(data[key])
            del data[key]
        data[self.__config.new_key] = value_list
        return data
