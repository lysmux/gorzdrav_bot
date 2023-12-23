from sqlalchemy import Integer, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.gorzdrav_api.schemas import (
    District, Clinic, Speciality, Doctor
)
from .base import BaseModel
from .user import UserModel
from ..types import PydanticType


class TrackingModel(BaseModel):
    __tablename__ = "tracking"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[UserModel] = relationship(backref="tracking", lazy="selectin", uselist=False)

    time_ranges: Mapped[list[list[int]]] = mapped_column(ARRAY(Integer), nullable=False)

    district: Mapped[District] = mapped_column(PydanticType(District), nullable=False)
    clinic: Mapped[Clinic] = mapped_column(PydanticType(Clinic), nullable=False)
    speciality: Mapped[Speciality] = mapped_column(PydanticType(Speciality), nullable=False)
    doctor: Mapped[Doctor] = mapped_column(PydanticType(Doctor), nullable=False)
