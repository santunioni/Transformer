from typing import Any, Dict, Optional, Tuple

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class DinamizeUnpackConfig(ExtraHashableModel):
    __root__: Optional[Any]


class DinamizeUnpack(Transformer[DinamizeUnpackConfig]):
    def transform(self, data: Dict, metadata: Dict) -> Tuple[Dict, Dict]:
        dt = {
            "dinamize": {
                field.get("Name"): field.get("Value")
                for field in data.get("custom_fields", {}).values()
            }
        }
        dt["dinamize"].update(data.get("fixed_fields", {}))
        return dt, metadata
