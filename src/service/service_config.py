from typing import Dict, Sequence, Union

from pydantic import BaseModel, root_validator

from src.service.commands.any_config import AnyCommandConfig
from src.service.commands.map_keys import MapKeysConfig


class ServiceConfig(BaseModel):
    commands: Sequence[AnyCommandConfig] = []

    @root_validator(pre=True)
    def populate_commands(cls, values: dict):
        """Adapt ServiceConfig for backwards compatibility.
        Transforms
        {
            "mapping": {"...": "...."},
            "preserve_unmapped: True
        }
        into
        {
            "commands": [
                {
                    "mapping": {"...": "...."},
                    "preserve_unmapped: True
                }
            ]
        }
        before initializing the pydantic object.
        """
        mapping = values.get("mapping")
        preserve_unmapped = values.get("preserve_unmapped", True)
        commands = values.get("commands", [])
        if mapping is not None:
            commands.insert(0, {
                "mapping": mapping,
                "preserve_unmapped": preserve_unmapped
            })
            values.pop("mapping")
        values["commands"] = commands
        return values
