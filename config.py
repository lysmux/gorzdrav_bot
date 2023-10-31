from enum import StrEnum

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

import secrets


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    database: str


class BotSettings(BaseModel):
    token: str


class WebhookSettings(BaseModel):
    host: str
    path: str = "/webhook"
    secret: str = secrets.token_urlsafe(32)

    app_host: str = "0.0.0.0"
    app_port: int = 8080


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str | None = None


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class Settings(BaseSettings):
    log_level: LogLevel = LogLevel.INFO

    use_redis: bool = False
    use_webhook: bool = False
    check_every: int = 5

    bot: BotSettings
    db: DatabaseSettings
    redis: RedisSettings = RedisSettings()
    webhook: WebhookSettings | None = None

    @field_validator("webhook")
    def check_web_hook(cls, value, info: ValidationInfo):
        if info.data.get("use_webhook") and value is None:
            raise ValueError("Settings for WebHook should be provided")
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        env_nested_delimiter = "__"
        env_prefix = "gorzdrav_"
        use_enum_values = True
