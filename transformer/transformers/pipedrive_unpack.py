from typing import Any, Dict, Optional, Tuple

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class PipedriveUnpackConfig(ExtraHashableModel):
    __root__: Optional[Any]


class PipedriveUnpack(Transformer[PipedriveUnpackConfig]):
    def transform(self, data: Dict, metadata: Dict) -> Tuple[Dict, Dict]:
        _object = data.get("meta", {}).get("object")
        r_data = {
            "pipedrive": {
                f"{_object}": {
                    key: value for key, value in data.get("current", {}).items()
                },
                "company": {"id": data.get("meta", {}).get("company_id")},
            }
        }
        r_metadata = {
            key: value
            for key, value in data.get("meta", {}).items()
            if key in ("action", "change_source", "company_id", "host", "id")
        }
        r_metadata.update({"origin": "pipedrive", "object": _object})
        r_metadata.update(metadata)
        return r_data, r_metadata
