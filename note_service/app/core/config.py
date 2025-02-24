"""
Конфигурация приложения с использованием pydantic-settings.
Значения конфигурации загружаются из переменных окружения и файла .env.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    database_name: str = "note_service_db"
    log_level: str = "INFO"
    service_name: str = "note_service"
    environment: str = "development"  # Опции: development, production, test
    sentry_dsn: Optional[str] = None  # Опциональный Sentry DSN для мониторинга ошибок

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()
