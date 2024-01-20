from pydantic import BaseModel


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str | None = None
