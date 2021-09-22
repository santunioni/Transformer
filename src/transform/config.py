from pydantic import root_validator
from the_flash import BaseHashableModel

from .chain import TransformerChainConfig


class TransformConfig(BaseHashableModel):
    transforms: TransformerChainConfig

    @root_validator(pre=True)
    def populate_transform(cls, values: dict):
        """
        Adapt ServiceConfig for backwards compatibility.
        Transforms
        {
            "mapping": {"...": "...."},
            "preserve_unmapped: True
        }
        into
        {
            "transforms": [
                {
                    "mapping": {"...": "...."},
                    "preserve_unmapped: True
                }
            ]
        }
        before initializing the pydantic object.
        :param values:
        :return:
        """
        mapping = values.get("mapping")
        preserve_unmapped = values.get("preserve_unmapped", True)
        transforms = values.get("transforms", [])
        if mapping is not None:
            transforms.insert(0, {
                "command_name": "map-keys",
                "mapping": mapping,
                "preserve_unmapped": preserve_unmapped
            })
            values.pop("mapping")
        values["transforms"] = transforms
        return values
