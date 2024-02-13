import re

from pydantic import computed_field, Field

from .base import Model


class Doctor(Model):
    id: str
    name: str
    area: str | None = Field(alias="ariaNumber")
    free_appointments: int = Field(alias="freeParticipantCount")

    @computed_field  # type: ignore[misc]
    @property
    def short_name(self) -> str:
        return re.sub(r"(?<= \w)\w+", ".", self.name)
