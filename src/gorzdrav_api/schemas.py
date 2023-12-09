import re
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    ConfigDict
)


class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)


class District(Model):
    id: str
    name: str


class Clinic(Model):
    id: str
    address: str | None
    full_name: str = Field(alias="lpuFullName")
    short_name: str = Field(alias="lpuShortName")


class Speciality(Model):
    id: str
    name: str


class Doctor(Model):
    id: str
    name: str
    area: str | None = Field(alias="ariaNumber")
    free_appointments: int = Field(alias="freeParticipantCount")

    @computed_field
    @property
    def short_name(self) -> str:
        return re.sub(r"(?<= \w)\w+", ".", self.name)


class Appointment(Model):
    id: str
    time: datetime = Field(alias="visitStart")

    @computed_field
    @property
    def time_str(self) -> str:
        return self.time.strftime("%d.%m.%Y в %H:%M")
