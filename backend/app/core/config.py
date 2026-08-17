from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "PelitaGuard"
    API_V1_STR: str = "/api/v1"

    # Kredensial akan otomatis diambil dari .env atau Environment Variable
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Supabase Connection
    DATABASE_URL: str

    # Groq AI
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    # Konfigurasi Pydantic Settings untuk membaca file .env
    model_config = SettingsConfigDict(
        # Mencari file .env di folder tempat main.py dijalankan
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

# Inisialisasi settings
settings = Settings()
