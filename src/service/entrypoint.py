from typing import Optional

from src.service.transform.collection import get_transformer, AtomicTransformerException
from src.the_flash.models.mat_events import ServiceLetter, ServiceResponse


async def default_letter_handler(letter: ServiceLetter) -> Optional[ServiceResponse]:
    """
    This function is responsible for getting the transformations that should be perfomed (specified in the letter)
    and calling the transform method whichever transformer was selected.
    :param letter: A ServiceLetter having the config to select the transform and the data that should be transformed,
    and also metadata.
    :return: Returns the ServiceResponse containing the transformed data.
    """

    """the config that is passed in here is a list of config for each transform that shall be performed"""
    transformer = get_transformer(letter.config.transforms)

    """Response class is instantiated"""
    response = ServiceResponse.from_letter(letter)

    """The data that is returned here is the data after all transformations. All transformations specified by the
    the config list were called in a chain sequence until the final form of the data has been reached."""
    try:
        response.data = transformer.transform(letter.data, letter.metadata)
        return response
    except AtomicTransformerException:
        return None
