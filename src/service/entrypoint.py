from typing import Optional

from src.service.transform.collection import get_transformer
from src.the_flash.models.mat_events import ServiceLetter, ServiceResponse


async def default_letter_handler(letter: ServiceLetter) -> Optional[ServiceResponse]:
    transformer = get_transformer(letter.config.commands)
    response = ServiceResponse.from_letter(letter)
    response.data = transformer.transform(letter.data, letter.metadata)
    return response
