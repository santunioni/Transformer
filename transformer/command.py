from typing import Sequence

from pydantic import BaseModel

from transformer.registry import COMMAND_NAMES, get_transformer
from transformer.transformers.abstract import ExtraHashableModel, Transformer
from transformer.transformers.chain import TransformerChain


class Command(ExtraHashableModel):
    name: COMMAND_NAMES
    config: ExtraHashableModel

    def get_transformer(self) -> Transformer:
        return get_transformer(self)


class ChainCommand(BaseModel):
    __root__: Sequence[Command]

    def get_transformer(self) -> TransformerChain:
        return TransformerChain(
            (command.get_transformer() for command in self.__root__)
        )
