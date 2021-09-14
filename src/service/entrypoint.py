from typing import Optional

from src.service.actuator import CommandActuator
from src.the_flash.models.mat_events import ServiceLetter, ServiceResponse


async def transform(letter: ServiceLetter) -> Optional[ServiceResponse]:
    actuator = CommandActuator()
    actuator.configure(service_letter=letter)
    actuator.execute_all_commands()
    response = ServiceResponse.from_letter(letter)
    response.data = letter.data
    return response
