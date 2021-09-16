from __future__ import annotations

from functools import lru_cache
from typing import Sequence, Union, Type

from src.service.transform.abstract import Transformer, BaseTransformerConfig
from src.service.transform.commands.add_key import AddKeyValueConfig, AddKeyValue
from src.service.transform.commands.aggregate_keys import AggregateKeyValue, AggregateKeyValueConfig
from src.service.transform.commands.del_key import DeleteKeyConfig, DeleteKey
from src.service.transform.commands.map_keys import MapKeysConfig, MapKeys
from src.service.transform.commands.empiricus_change import EmpiricusChangeKeyValueConfig, EmpiricusChangeKeyValue


class TransformerCollectionConfig(BaseTransformerConfig):
    __root__: Sequence[AnyTransformerConfig]


class TransformerCollection(Transformer):

    def __init__(self, config: TransformerCollectionConfig):
        super().__init__(config)
        self.__transformers = tuple(map(get_transformer, config.__root__))

    def transform(self, data: dict, metadata: dict) -> dict:
        for transformer in self.__transformers:
            data = transformer.transform(data, metadata)
        return data


AnyTransformerConfig = Union[
    MapKeysConfig,
    DeleteKeyConfig,
    EmpiricusChangeKeyValueConfig,
    AggregateKeyValueConfig,
    AddKeyValueConfig,
    TransformerCollectionConfig
]


CONFIG_NAME_TO_TRANSFORMER_CLASS: dict[str, Type[Transformer]] = {
    MapKeysConfig.__name__: MapKeys,
    EmpiricusChangeKeyValueConfig.__name__: EmpiricusChangeKeyValue,
    AddKeyValueConfig.__name__: AddKeyValue,
    DeleteKeyConfig.__name__: DeleteKey,
    AggregateKeyValueConfig.__name__: AggregateKeyValue,
    TransformerCollectionConfig.__name__: TransformerCollection
}


TransformerCollectionConfig.update_forward_refs()


@lru_cache
def get_transformer(config: BaseTransformerConfig) -> Transformer:
    return CONFIG_NAME_TO_TRANSFORMER_CLASS[config.__class__.__name__](config)
