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

    # --- Database (PostgreSQL) ---
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost/aria",
        alias="DATABASE_URL"
    )

    # --- Redis ---
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # --- Vector DB (Chroma) ---
    chroma_path: str = Field(default="./data/chroma_db", alias="CHROMA_PATH")

    # --- AI (General) ---
    ai_provider: str = Field(default="ollama", alias="AI_PROVIDER")

    # --- AI (Ollama) ---
    ollama_host: str = Field(default="http://localhost:11434", alias="OLLAMA_HOST")
    ollama_model: str = Field(default="llama3.2", alias="OLLAMA_MODEL")

    # --- AI (Gemini) ---
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash", alias="GEMINI_MODEL")

    # --- OCR (Tesseract) ---
    tesseract_path: str = Field(
        default=r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        alias="TESSERACT_PATH"
    )

    # --- Storage (MinIO) ---
    minio_endpoint: str = Field(default="localhost:9000", alias="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minioadmin", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", alias="MINIO_SECRET_KEY")
    minio_secure: bool = Field(default=False, alias="MINIO_SECURE")
    minio_bucket_name: str = Field(default="aria-storage", alias="MINIO_BUCKET_NAME")

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
