from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret: str = ""
    llm: str = ""
    reasoning_llm: str = ""
    metadata: dict[str, Any] = {}
    model_config = SettingsConfigDict(env_file="../../.env")


settings = Settings()
