from enum import StrEnum

from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

from .bot import BotSettings
from .database import DatabaseSettings
from .redis import RedisSettings
from .webhook import WebhookSettings


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"

    @classmethod
    def _missing_(cls, value: str):  # type: ignore
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

    admins: list[int] = []

    bot: BotSettings
    db: DatabaseSettings
    redis: RedisSettings | None = None
    webhook: WebhookSettings | None = None

    @field_validator("redis")
    def check_redis(cls, value, info: ValidationInfo):
        if info.data.get("use_redis") and value is None:
            return RedisSettings()
        return value

    @field_validator("webhook")
    def check_webhook(cls, value, info: ValidationInfo):
        if info.data.get("use_webhook") and value is None:
            raise ValueError("Settings for WebHook should be provided")
        return value

    class Config:
        use_enum_values = True

        env_file = ".env"
        env_file_encoding = "utf-8"

        env_nested_delimiter = "__"
        env_prefix = "gorzdrav_"
