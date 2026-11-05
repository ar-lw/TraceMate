from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_provider: Literal["gemini", "ollama"] = "gemini"
    embedding_provider: Literal["gemini", "ollama"] = "gemini"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-flash-latest"
    gemini_embedding_model: str = "gemini-embedding-001"

    ollama_base_url: str = "http://localhost:11434"
    ollama_llm_model: str = "qwen2.5:3b"
    ollama_embedding_model: str = "nomic-embed-text"


@lru_cache
def get_settings() -> Settings:
    return Settings()
