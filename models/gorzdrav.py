from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseItem:
    id: str
    name: str


@dataclass
class District(BaseItem):
    pass


@dataclass
class Clinic(BaseItem):
    pass


@dataclass
class Speciality(BaseItem):
    pass


@dataclass
class Doctor(BaseItem):
    pass


@dataclass
class Appointment:
    id: str
    datetime: datetime
