from typing import Dict, Tuple

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class PipedriveUnpackConfig(ExtraHashableModel):
    ...


class PipedriveUnpack(Transformer[PipedriveUnpackConfig]):
    def transform(self, data: Dict, metadata: Dict) -> Tuple[Dict, Dict]:
        metadata.update(
            {
                k: v
                for k, v in data.get("meta", {}).items()
                if k
                in ("action", "change_source", "company_id", "host", "id", "object")
            }
        )
        metadata.update(
            {"origin": "pipedrive", "type": data.get("meta", {}).get("object")}
        )
        return data.get("current", {}), metadata
