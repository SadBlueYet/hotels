from typing import ClassVar

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(find_dotenv(".env"))



class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    class LLM(BaseSettings):
        LLM_MODEL: str = "gpt-4o"
        OPENAI_API_KEY: str = ""

    llm: ClassVar[LLM] = LLM()


settings = Settings()
