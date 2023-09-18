from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from urllib.parse import quote


class District(BaseModel):
    id: str
    name: str


class Clinic(BaseModel):
    id: int
    address: str
    full_name: str = Field(alias="lpuFullName")
    short_name: str = Field(alias="lpuShortName")


class Speciality(BaseModel):
    id: str
    name: str

    # noinspection PyMethodParameters
    @field_validator("id")
    def id_fix(cls, value: str):
        value = quote(value, safe="")
        return value


class Doctor(BaseModel):
    id: str
    name: str
    free_appointments: int = Field(alias="freeParticipantCount")
    nearest_appointment: datetime | None = Field(alias="nearestDate")


class Appointment(BaseModel):
    id: str
    room: str
    time: datetime = Field(alias="visitStart")
