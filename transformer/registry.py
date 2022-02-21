from functools import lru_cache
from typing import Any, Literal, Mapping, Protocol, Tuple, Type

from transformer.transformers.abstract import ExtraHashableModel, Transformer
from transformer.transformers.add_key import AddKeyValues, AddKeyValuesConfig
from transformer.transformers.aggregate_keys import (
    AggregateKeyValue,
    AggregateKeyValueConfig,
)
from transformer.transformers.del_key import DeleteKeys, DeleteKeysConfig
from transformer.transformers.flatters import Flatter, FlatterConfigPydantic, Unflatter
from transformer.transformers.map_keys import MapKeys, MapKeysConfig
from transformer.transformers.value_sanitizer import (
    ValueSanitizer,
    ValueSanitizerConfig,
)

#   It's important to registry all transformers provided by the lib here,
# aiming automatic instantiation of transformers
CommandNames = Literal[
    "map-keys",
    "value-sanitizer",
    "delete-keys",
    "aggregate-keys",
    "add-key-values",
    "flatten",
    "unflatten",
]
NAME_TO_CONFIG_AND_TRANSFORM_CLASSES: Mapping[
    CommandNames, Tuple[Type[ExtraHashableModel], Type[Transformer]]
] = {
    "flatten": (FlatterConfigPydantic, Flatter),
    "unflatten": (FlatterConfigPydantic, Unflatter),
    "map-keys": (MapKeysConfig, MapKeys),
    "value-sanitizer": (ValueSanitizerConfig, ValueSanitizer),
    "delete-keys": (DeleteKeysConfig, DeleteKeys),
    "aggregate-keys": (AggregateKeyValueConfig, AggregateKeyValue),
    "add-key-values": (AddKeyValuesConfig, AddKeyValues),
}


class _Command(Protocol):
    name: CommandNames
    config: Any

    def __hash__(self) -> int:
        ...


@lru_cache
def get_transformer(command: _Command) -> Transformer:
    config_class, transformer_class = NAME_TO_CONFIG_AND_TRANSFORM_CLASSES[command.name]
    config = config_class.parse_obj(command.config)
    transformer = transformer_class(config)
    return transformer


__all__ = ["CommandNames", "NAME_TO_CONFIG_AND_TRANSFORM_CLASSES", "get_transformer"]
