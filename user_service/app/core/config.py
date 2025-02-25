from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    mongo_url: str
    database_name: str
    log_level: str
    service_name: str
    environment: str
    rabbitmq_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    sentry_dsn: Optional[str] = None
    auth_token_url: str = "http://localhost:8001/api/auth/login"

    model_config = SettingsConfigDict(
        env_file=".env.user_service",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()