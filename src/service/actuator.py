from typing import Type, Sequence

from src.service.abstractions import TransformCommand
from src.service.commands.any_config import AnyCommandConfig
from src.service.commands.map_keys import MapKeysConfig, MapKeys
from src.the_flash.models.mat_events import ServiceLetter

CONFIG_TO_COMMAND_DICT: dict[str, Type[TransformCommand]] = {
    MapKeysConfig.__name__: MapKeys
}


class CommandActuator(TransformCommand):

    def __init__(self, configs: Sequence[AnyCommandConfig]):
        self.__transformers: list[TransformCommand] = [
            CONFIG_TO_COMMAND_DICT[config.__class__.__name__](
                config=config
            ) for config in configs
        ]

    def transform(self, data: dict, metadata: dict) -> dict:
        for transformer in self.__transformers:
            data = transformer.transform(data, metadata)
        return data

    def configure(self, service_letter: ServiceLetter):
        for config in service_letter.config.commands:
            self.__transformers.append(
                CONFIG_TO_COMMAND_DICT[config.__class__.__name__](
                    receiver=service_letter,
                    config=config
                )
            )
