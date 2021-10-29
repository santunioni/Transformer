from typing import Any, Dict, Optional, Tuple

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class DinamizeUnpackConfig(ExtraHashableModel):
    __root__: Optional[Any]


class DinamizeUnpack(Transformer[Any]):
    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        return_data = {
            "dinamize": {
                field.get("Name"): field.get("Value")
                for field in payload.get("custom_fields", {}).values()
            }
        }
        return_data["dinamize"].update(payload.get("fixed_fields", {}))
        return return_data, metadata or {}
