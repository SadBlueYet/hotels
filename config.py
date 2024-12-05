import logging
from typing import ClassVar

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    class Llm(BaseSettings):
        OPENAI_API_KEY: str = ""

    class FilesPaths(BaseSettings):
        JSON_AMENITIES_FILE_PATH: str = "files/amenities.json"
        JSON_HOTELS_FILE_PATH: str = "files/hotels.json"
        JSON_OUTPUT_FILE_PATH: str = "files/output.json"

    class Logging:
        LOG_LEVEL: str = "INFO"
        LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def setup_logging(self):
        logging.basicConfig(
            level=self.Logging.LOG_LEVEL, format=self.Logging.LOG_FORMAT
        )

    LLM: ClassVar[Llm] = Llm()
    LOGGING: ClassVar[Logging] = Logging()
    FILES_PATHS: ClassVar[FilesPaths] = FilesPaths()


settings = Settings()
settings.setup_logging()
