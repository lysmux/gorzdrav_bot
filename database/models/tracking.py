from sqlalchemy import Integer, Column, ARRAY

from database.models.base import Base
from database.types import PydanticType
from gorzdrav_api.schemas import District, Clinic, Speciality, Doctor


class Tracking(Base):
    __tablename__ = "tracking"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=False)

    time_ranges = Column(ARRAY(Integer), nullable=False)

    district = Column(PydanticType(District), nullable=False)
    clinic = Column(PydanticType(Clinic), nullable=False)
    speciality = Column(PydanticType(Speciality), nullable=False)
    doctor = Column(PydanticType(Doctor), nullable=False)

    def __repr__(self):
        return (f"<Tracking("
                f"id={self.id}, "
                f"tg_user_id={self.tg_user_id}, "
                f"time_ranges={self.time_ranges}, "
                f"district={self.district}, "
                f"clinic={self.clinic}, "
                f"speciality={self.speciality}"
                f"doctor={self.doctor})>")

