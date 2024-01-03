from pydantic import Field

from .base import Model


class Clinic(Model):
    id: str
    address: str | None
    full_name: str = Field(alias="lpuFullName")
    short_name: str = Field(alias="lpuShortName")
