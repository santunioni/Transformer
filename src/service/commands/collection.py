from functools import lru_cache
from typing import Sequence, Union, Type

from src.service.commands.abstract import TransformerConfig, Transformer
from src.service.commands.map_keys import MapKeysConfig, MapKeys

AnyTransformerConfig = Union[MapKeysConfig]


class TransformerCollectionConfig(TransformerConfig):
    __root__: Sequence[AnyTransformerConfig]


class TransformerCollection(Transformer):

    def __init__(self, config: TransformerCollectionConfig):
        super().__init__(config)
        self.__transformers = tuple(map(get_transformer, config.__root__))

    def transform(self, data: dict, metadata: dict) -> dict:
        for transformer in self.__transformers:
            data = transformer.transform(data, metadata)
        return data


CONFIG_NAME_TO_TRANSFORMER_CLASS: dict[str, Type[Transformer]] = {
    MapKeysConfig.__name__: MapKeys,
    TransformerCollectionConfig.__name__: TransformerCollection
}


@lru_cache
def get_transformer(config: TransformerConfig) -> Transformer:
    return CONFIG_NAME_TO_TRANSFORMER_CLASS[config.__class__.__name__](config)
