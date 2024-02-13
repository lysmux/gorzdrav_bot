import secrets

from pydantic import BaseModel, computed_field


class WebhookSettings(BaseModel):
    domain: str
    path: str
    secret: str = secrets.token_urlsafe(32)

    app_host: str = "0.0.0.0"
    app_port: int = 8000

    @computed_field  # type: ignore[misc]
    @property
    def url(self) -> str:
        return "https://" + self.domain + self.path
