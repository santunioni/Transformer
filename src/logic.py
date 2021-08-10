import logging

from src.utils.mapping import map_keys
from src.models.mat_events import ServiceLetter, ServiceResponse
from src.settings import EnvironmentSettings

logger = logging.getLogger(__name__)


async def process_message(letters, response, settings: EnvironmentSettings):
    while True:
        service_letter: ServiceLetter = await letters.get()
        service_response = ServiceResponse.from_service_letter(service_letter)
        data_mapping = map_keys(data=service_letter.data,
                                mapping=service_letter.config.mapping,
                                preserve_unmapped=service_letter.config.preserve_unmapped)

        service_response.data = data_mapping
        await response.put(service_response)
        letters.task_done()
