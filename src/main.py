from typing import Optional

from dotenv import load_dotenv, find_dotenv
from the_flash import TheFlash, ServiceResponse, ServiceLetter

from src.service_config import TransformConfig
from src.transform.collection import get_transformer


def transform_data(letter: ServiceLetter[TransformConfig]) -> Optional[ServiceResponse]:
    transformer = get_transformer(letter.config.transforms)
    response = ServiceResponse.from_letter(letter)
    response.data = transformer.transform(letter.data, letter.metadata)
    return response


if __name__ == "__main__":
    load_dotenv(find_dotenv("local.env"))
    app = TheFlash(config_parser=TransformConfig)
    app.letter_handlers.set_default(transform_data)
    app.start()
