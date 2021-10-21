from functools import lru_cache
from typing import Any, Literal, Mapping, Protocol, Tuple, Type

from transformer.transformers.abstract import ExtraHashableModel, Transformer
from transformer.transformers.add_key import AddKeyValues, AddKeyValuesConfig
from transformer.transformers.aggregate_keys import (
    AggregateKeyValue,
    AggregateKeyValueConfig,
)
from transformer.transformers.del_key import DeleteKeys, DeleteKeysConfig
from transformer.transformers.map_keys import MapKeys, MapKeysConfig
from transformer.transformers.value_sanitizer import (
    ValueSanitizer,
    ValueSanitizerConfig,
)

#   It's important to registry all transformers provided by the lib here,
# aiming automatic instantiation of transformers
COMMAND_NAMES = Literal[
    "map-keys",
    "value-sanitizer",
    "delete-keys",
    "aggregate-keys",
    "add-key-values",
]
NAME_TO_CONFIG_AND_TRANSFORM_CLASSES: Mapping[
    COMMAND_NAMES, Tuple[Type[ExtraHashableModel], Type[Transformer]]
] = {
    "map-keys": (MapKeysConfig, MapKeys),
    "value-sanitizer": (ValueSanitizerConfig, ValueSanitizer),
    "delete-keys": (DeleteKeysConfig, DeleteKeys),
    "aggregate-keys": (AggregateKeyValueConfig, AggregateKeyValue),
    "add-key-values": (AddKeyValuesConfig, AddKeyValues),
}


class _Command(Protocol):
    name: COMMAND_NAMES
    config: Any

    def __hash__(self):
        ...


@lru_cache
def get_transformer(command: _Command) -> Transformer:
    config_class, transformer_class = NAME_TO_CONFIG_AND_TRANSFORM_CLASSES[command.name]
    config = config_class.parse_obj(command.config)
    transformer = transformer_class(config)
    return transformer


__all__ = ["COMMAND_NAMES", "NAME_TO_CONFIG_AND_TRANSFORM_CLASSES", "get_transformer"]
