import logging

from pydantic import BaseSettings

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)s - %(message)s',
    level=logging.INFO)


class EnvironmentSettings(BaseSettings):
    MAX_CONCURRENT_MESSAGES: int = 2000
    CONCURRENT_TASKS: int = 1000
