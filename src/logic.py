import logging
from asyncio import Queue

from src.models.mat_events import ServiceLetter, ServiceResponse
from src.utils.mapping import map_keys

logger = logging.getLogger(__name__)


async def process_message(letters: Queue[ServiceLetter], responses: Queue[ServiceResponse]):
    while True:
        service_letter: ServiceLetter = await letters.get()
        service_response = ServiceResponse.from_service_letter(service_letter)

        try:
            mapped_data, unmapped_data = map_keys(
                data=service_letter.data,
                mapping=service_letter.config.mapping,
                preserve_unmapped=service_letter.config.preserve_unmapped
            )

            if not service_letter.config.preserve_unmapped and unmapped_data != {}:
                logger.warning("Unmapped data for event_trace=%s: %s", service_letter.event_trace, str(unmapped_data))

            service_response.data = mapped_data
            await responses.put(service_response)
        except Exception:
            logger.critical("Some general exception occurred", exc_info=True)

        letters.task_done()
