from pydantic import BaseModel, root_validator

from src.service.transform.collection import TransformerCollectionConfig


class ServiceConfig(BaseModel):
    commands: TransformerCollectionConfig

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
            "transform": [
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
        commands = values.get("transform", [])
        if mapping is not None:
            commands.insert(0, {
                "mapping": mapping,
                "preserve_unmapped": preserve_unmapped
            })
            values.pop("mapping")
        values["transform"] = commands
        return values
