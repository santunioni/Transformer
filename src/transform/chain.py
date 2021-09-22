from __future__ import annotations

import logging
from functools import lru_cache
from typing import Sequence, Union, Type

from the_flash import BaseHashableModel

from .abstract import Transformer
from .commands.add_key import AddKeyValuesConfig, AddKeyValues
from .commands.aggregate_keys import AggregateKeyValueConfig, AggregateKeyValue
from .commands.del_key import DeleteKeysConfig, DeleteKeys
from .commands.map_keys import MapKeysConfig, MapKeys
from .commands.value_sanitizer import ValueSanitizerConfig, ValueSanitizer

logger = logging.getLogger(__name__)


class TransformerChainConfig(BaseHashableModel):
    __root__: Sequence[AnyTransformerConfig]


class AtomicTransformerException(Exception):
    ...


class TransformerChain(Transformer):
    """
    This class is fundamental to the sequential calls of Transformer.
    The config json will come as a list of calls to transformers. get_transformer method will then
    instantiate this class first.
    This class is called first
    """

    def __init__(self, config: TransformerChainConfig):
        super().__init__(config)
        self.__transformers = tuple(map(get_transformer, config.__root__))

    def transform(self, data: dict, metadata: dict) -> dict:
        """
        This is actually a chain that will call each transformer in the first config list and pass its result
        (the transformed data) to the next transformer.
        :param data: Initial untransformed data.
        :param metadata: Metadata
        :return: data to be inserted in the ServiceResponse object.
        """
        data_copy = data.copy()
        try:
            for transformer in self.__transformers:
                data_copy = transformer.transform(data_copy, metadata)
            return data_copy
        except Exception as err:
            logger.warning("...", exc_info=True)
            raise AtomicTransformerException from err


"""This is all types of transformers. New Transformers should have its type here in order to pydantic do its job."""
AnyTransformerConfig = Union[
    MapKeysConfig,
    DeleteKeysConfig,
    AggregateKeyValueConfig,
    AddKeyValuesConfig,
    TransformerChainConfig,
    ValueSanitizerConfig
]

"""Its important to notice that this dictionary is responsible for getting a class out of the config.
New Transformers must have its mapping here in order to work properly."""
CONFIG_NAME_TO_TRANSFORMER_CLASS: dict[str, Type[Transformer]] = {
    MapKeysConfig.__name__: MapKeys,
    AddKeyValuesConfig.__name__: AddKeyValues,
    DeleteKeysConfig.__name__: DeleteKeys,
    AggregateKeyValueConfig.__name__: AggregateKeyValue,
    TransformerChainConfig.__name__: TransformerChain,
    ValueSanitizerConfig.__name__: ValueSanitizer
}

"""This only exists because TransformerChain has a reference to itself during its creation"""
TransformerChainConfig.update_forward_refs()


@lru_cache
def get_transformer(config: BaseHashableModel) -> Transformer:
    """
    This function is responsible for getting a transformer. The first time it is called in the entrypoint it will
    be used to call the TransformerChain, which in turn, calls this functions as many times as requested in the
    config list.

    *****
    It's important to understand that we are relying on Pydantic's parse capabilities.
    The configs for each Transformer are passed on a list from ServiceLetter.
    When get_transformer is called with a config that is a list of configs it can only calls the
    TransformerChain, since its the only one that accepts a list as argument.
    ****

    ****
    This function is chached by @lru_cache in order to get_transformer keep the result in memory if future calls are
    made with the same arguments. This is important since configs are repetitive.
    ****

    :param config: The config can be a list of configs, that triggers a call to TransformCollection. Or a single
    config, which triggers a call to other specific transformer.
    :return: a Tranformer object, the transformer object is uniquely identified by its name. Pydantic will only be able
    to parse to a transformer whose name selected on config is the same name in the TransformerConfig
    """
    return CONFIG_NAME_TO_TRANSFORMER_CLASS[config.__class__.__name__](config)
