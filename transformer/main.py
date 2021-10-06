import os
from typing import Optional

from the_flash import ServiceLetter, ServiceResponse, TheFlash

from transformer.chain import AtomicTransformerException, get_transformer
from transformer.config import TransformConfig


def transform_data(letter: ServiceLetter[TransformConfig]) -> Optional[ServiceResponse]:
    """
    This function is responsible for getting the transformations that should be performed (specified in the letter)
    and calling the transformer method whichever transformer was selected.
    :param letter: A ServiceLetter having the config to select the transformer and the data that should be transformed,
    and also metadata.
    :return: Returns the ServiceResponse containing the transformed data.
    """

    transformer = get_transformer(letter.config.transforms)
    response = ServiceResponse.from_letter(letter)
    try:
        response.data = transformer.transform(letter.data, letter.metadata)
        return response
    except AtomicTransformerException:
        return None


def main() -> None:
    os.environ["SERVICE_NAME"] = "json-transformer"
    os.environ["SERVICE_VERSION"] = "2.0.1"

    app = TheFlash(config_parser=TransformConfig)
    app.letter_handlers.set_default(transform_data)
    app.start()


if __name__ == "__main__":
    main()
