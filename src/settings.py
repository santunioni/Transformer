import logging

from pydantic import BaseSettings

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)s - %(message)s',
    level=logging.INFO
)


class EnvironmentSettings(BaseSettings):
    NUMBER_OF_MAX_CONCURRENT_MESSAGES: int = 0
    NUMBER_OF_CONCURRENT_SERVICE_CALLS: int = 1000
