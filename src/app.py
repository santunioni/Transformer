from typing import Optional

from the_flash import TheFlash, ServiceResponse, ServiceLetter

from src.transform.service_config import TransformConfig
from src.transform.collection import get_transformer


def transform_data(letter: ServiceLetter[TransformConfig]) -> Optional[ServiceResponse]:
    transformer = get_transformer(letter.config.transforms)
    response = ServiceResponse.from_letter(letter)
    response.data = transformer.transform(letter.data, letter.metadata)
    return response


app = TheFlash(config_parser=TransformConfig)
app.letter_handlers.set_default(transform_data)
