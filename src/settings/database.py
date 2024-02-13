from pydantic import computed_field, BaseModel
from sqlalchemy import URL


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    database: str

    @computed_field  # type: ignore[misc]
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
