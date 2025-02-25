from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    mongo_url: str
    database_name: str
    log_level: str
    service_name: str
    environment: str
    jwt_secret_key: str
    jwt_algorithm: str
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"  # Добавляем по умолчанию
    sentry_dsn: Optional[str] = None
    auth_token_url: str = "http://localhost:8001/api/auth/login"

    model_config = SettingsConfigDict(
        env_file=".env.example",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()