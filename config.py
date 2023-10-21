import secrets

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    database: str


class BotSettings(BaseModel):
    token: str


class WebhookSettings(BaseModel):
    url: str
    path: str
    secret: str = secrets.token_urlsafe(32)

    server_host: str = "localhost"
    server_port: int


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str | None = None


class Settings(BaseSettings):
    use_redis: bool = False
    use_webhook: bool = False
    check_every: int = 5

    bot: BotSettings
    db: DatabaseSettings
    redis: RedisSettings
    webhook: WebhookSettings

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
