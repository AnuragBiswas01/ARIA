"""
ARIA Configuration Management
Loads settings from environment variables and .env file.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- API ---
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # --- Ollama ---
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.2:3b-instruct-q4_K_M", alias="OLLAMA_MODEL")

    # --- Database ---
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/memory/aria_memory.db",
        alias="DATABASE_URL"
    )
    chroma_persist_dir: str = Field(
        default="./data/memory/chroma",
        alias="CHROMA_PERSIST_DIR"
    )

    # --- Memory Settings ---
    working_memory_size: int = Field(default=10, alias="WORKING_MEMORY_SIZE")
    short_term_memory_ttl_hours: int = Field(default=6, alias="SHORT_TERM_MEMORY_TTL_HOURS")

    # --- Home Assistant (Optional) ---
    hass_url: str | None = Field(default=None, alias="HASS_URL")
    hass_token: str | None = Field(default=None, alias="HASS_TOKEN")

    # --- Piper TTS (Optional) ---
    piper_voice_model: str = Field(default="en_US-lessac-medium", alias="PIPER_VOICE_MODEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Returns cached settings instance."""
    return Settings()


# Export a singleton for easy access
settings = get_settings()
