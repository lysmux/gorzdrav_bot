from dataclasses import dataclass
from datetime import datetime

from utils.datetime_to_str import datetime_to_str


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
class Appointment(BaseItem):
    datetime: datetime

    def __post_init__(self):
        self.name = datetime_to_str(self.datetime)
