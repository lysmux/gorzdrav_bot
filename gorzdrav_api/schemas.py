from datetime import datetime

from pydantic import BaseModel, Field, computed_field, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class District(Model):
    id: str
    name: str


class Clinic(Model):
    id: int
    address: str
    full_name: str = Field(alias="lpuFullName")
    short_name: str = Field(alias="lpuShortName")


class Speciality(Model):
    id: str
    name: str


class Doctor(Model):
    id: str
    name: str
    free_appointments: int = Field(alias="freeParticipantCount")


class Appointment(Model):
    id: str
    room: str
    time: datetime = Field(alias="visitStart")

    @computed_field
    @property
    def time_str(self) -> str:
        return self.time.strftime("%d.%m.%Y в %H:%M")
