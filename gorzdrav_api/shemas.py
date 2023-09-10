from datetime import datetime

from pydantic import BaseModel, Field


class District(BaseModel):
    id: int
    name: str


class Clinic(BaseModel):
    id: int
    address: str
    full_name: str = Field(alias="lpuFullName")
    short_name: str = Field(alias="lpuShortName")


class Speciality(BaseModel):
    id: int
    name: str


class Doctor(BaseModel):
    id: int
    name: str
    free_appointments: int = Field(alias="freeParticipantCount")
    nearest_appointment: datetime = Field(alias="nearestDate")


class Appointment(BaseModel):
    id: int
    room: str
    time: datetime = Field(alias="visitStart")
