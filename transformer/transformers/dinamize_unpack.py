from typing import Dict, Tuple

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class DinamizeUnpackConfig(ExtraHashableModel):
    ...


class DinamizeUnpack(Transformer[DinamizeUnpackConfig]):
    def transform(self, data: Dict, metadata: Dict) -> Tuple[Dict, Dict]:
        dt = {
            field.get("Name"): field.get("Value")
            for field in data.get("custom_fields", {}).values()
        }
        dt.update(data.get("fixed_fields", {}))
        return dt, metadata
