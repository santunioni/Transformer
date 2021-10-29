from typing import Any, Dict, Iterable, Optional

from transformer.transformers.abstract import Transformer

TransformerChainConfig = Iterable[Transformer]


class TransformerChain(Transformer[TransformerChainConfig]):
    """
    This class is fundamental to the sequential calls of Transformer.
    The config json will come as a list of calls to transformers. get_transformer method will then
    instantiate this class first.
    This class is called first
    """

    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ):
        """
        This is actually a chain that will call each transformer in the first config list and pass its result
        (the transformed data) to the next transformer.
        :param payload: Initial untransformed data.
        :param metadata: Metadata
        :return: data to be inserted in the ServiceResponse object.
        """
        for transformer in self._config:
            payload, metadata = transformer.transform(payload, metadata or {})

        if metadata is None:
            return payload

        return payload, metadata
