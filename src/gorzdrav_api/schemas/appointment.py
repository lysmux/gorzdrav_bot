from datetime import datetime

from pydantic import Field, computed_field

from .base import Model


class Appointment(Model):
    id: str
    time: datetime = Field(alias="visitStart")

    @computed_field
    @property
    def time_str(self) -> str:
        return self.time.strftime("%d.%m.%Y в %H:%M")
