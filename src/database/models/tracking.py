from itertools import groupby
from operator import sub, itemgetter
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ARRAY, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.gorzdrav_api.schemas import (
    District, Clinic, Speciality, Doctor
)
from .base import BaseModel
from ..types import PydanticType

if TYPE_CHECKING:
    from .user import UserModel


class TrackingModel(BaseModel):
    __tablename__ = "tracking"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserModel"] = relationship(back_populates="tracking", lazy="selectin", uselist=False)

    hours: Mapped[set[int]] = mapped_column(ARRAY(Integer), nullable=False)

    district: Mapped[District] = mapped_column(PydanticType(District), nullable=False)
    clinic: Mapped[Clinic] = mapped_column(PydanticType(Clinic), nullable=False)
    speciality: Mapped[Speciality] = mapped_column(PydanticType(Speciality), nullable=False)
    doctor: Mapped[Doctor] = mapped_column(PydanticType(Doctor), nullable=False)

    @hybrid_property
    def time_ranges(self) -> list[list[int]]:
        result = []

        for k, g in groupby(enumerate(self.hours), lambda x: sub(*x)):
            items = list(map(itemgetter(1), g))
            if len(items) > 1:
                result.append([items[0], items[-1]])
            else:
                result.append([items[0], items[0]])

        return result
