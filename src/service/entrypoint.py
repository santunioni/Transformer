from typing import Optional

from src.the_flash.models.mat_events import ServiceLetter, ServiceResponse
from src.utils.mapping import map_keys


async def letter_entrypoint(letter: ServiceLetter) -> Optional[ServiceResponse]:
    mapped_data = map_keys(
        letter.data,
        mapping=letter.config.mapping,
        metadata=letter.metadata,
        preserve_unmapped=letter.config.preserve_unmapped
    )

    response = ServiceResponse.from_letter(letter)
    response.data = mapped_data
    return response
