from typing import Any, Dict, Optional, Tuple

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class PipedriveUnpackConfig(ExtraHashableModel):
    __root__: Optional[Any]


class PipedriveUnpack(Transformer[Any]):
    def __init__(self, config: Any = 0):
        super().__init__(config)

    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        _object = payload.get("meta", {}).get("object")
        r_data = {
            "pipedrive": {
                f"{_object}": payload.get("current", {}),
                "company": {"id": payload.get("meta", {}).get("company_id")},
            }
        }
        r_metadata = {
            key: value
            for key, value in payload.get("meta", {}).items()
            if key in ("action", "change_source", "company_id", "host", "id")
        }
        r_metadata.update({"origin": "pipedrive", "object": _object})
        r_metadata.update(metadata or {})
        return r_data, r_metadata
