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
    use_redis: bool = False


class Settings(BaseSettings):
    bot: BotSettings
    db: DatabaseSettings

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
