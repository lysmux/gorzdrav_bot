from datetime import datetime

from pydantic import BaseModel, Field


class District(BaseModel):
    id: int
    name: str


class Clinic(BaseModel):
    id: int
    full_name: str = Field(..., alias="lpuFullName")
    short_name: str = Field(..., alias="lpuShortName")
    address: str


class Speciality(BaseModel):
    id: int
    name: str
    free_appointments: int = Field(..., alias="countFreeParticipant")


class Doctor(BaseModel):
    id: int
    name: str
    free_appointments: int = Field(..., alias="freeParticipantCount")
    nearest_appointment: datetime = Field(..., alias="nearestDate")
    room: str = Field(..., alias="comment")


class Appointment(BaseModel):
    id: int
    time: datetime = Field(..., alias="visitStart")
