import secrets
from enum import StrEnum

from pydantic import BaseModel, field_validator, computed_field
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings
from sqlalchemy import URL


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


class BotSettings(BaseModel):
    token: str


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    database: str

    @computed_field
    @property
    def url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.database
        ).render_as_string(hide_password=False)


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str | None = None


class WebhookSettings(BaseModel):
    domain: str
    path: str
    secret: str = secrets.token_urlsafe(32)

    app_host: str = "0.0.0.0"
    app_port: int = 8000

    @computed_field
    @property
    def url(self) -> str:
        return "https://" + self.domain + self.path


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


settings = Settings()
