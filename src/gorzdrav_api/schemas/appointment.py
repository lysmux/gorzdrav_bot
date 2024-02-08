from datetime import datetime

from pydantic import Field, computed_field

from .base import Model


class Appointment(Model):
    id: str
    time: datetime = Field(alias="visitStart")

    @computed_field  # type: ignore[misc]
    @property
    def time_str(self) -> str:
        return self.time.strftime("%d.%m.%Y в %H:%M")

    def __hash__(self) -> int:
        return hash(self.id)
