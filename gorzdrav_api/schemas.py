from datetime import datetime

from pydantic import BaseModel, Field, computed_field


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


class Doctor(BaseModel):
    id: str
    name: str
    free_appointments: int = Field(alias="freeParticipantCount")


class Appointment(BaseModel):
    id: str
    room: str
    time: datetime = Field(alias="visitStart")

    @computed_field
    @property
    def time_str(self) -> str:
        return self.time.strftime("%d.%m.%Y в %H:%M")
