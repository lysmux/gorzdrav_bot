from sqlalchemy import Integer, Column, ARRAY

from database.models.base import Base
from database.types import PydanticType
from gorzdrav_api.schemas import District, Clinic, Speciality, Doctor


class Tracking(Base):
    __tablename__ = "tracking"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    tg_user_id = Column(Integer, nullable=False)

    hours = Column(ARRAY(Integer), nullable=False)

    district = Column(PydanticType(District), nullable=False)
    clinic = Column(PydanticType(Clinic), nullable=False)
    speciality = Column(PydanticType(Speciality), nullable=False)
    doctor = Column(PydanticType(Doctor), nullable=False)
