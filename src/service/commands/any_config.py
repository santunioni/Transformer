from typing import Sequence, Union

from src.service.commands.base_config import BaseCommandConfig
from src.service.commands.map_keys import MapKeysConfig

AnyCommandConfig = Union[MapKeysConfig]


class CommandConfigs(BaseCommandConfig):
    __root__: Sequence[AnyCommandConfig]
