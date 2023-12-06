from sqlalchemy import Integer, BigInteger, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base
from src.database.types import PydanticType
from src.gorzdrav_api import schemas


class Tracking(Base):
    __tablename__ = "tracking"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    time_ranges: Mapped[list[list[int]]] = mapped_column(ARRAY(Integer), nullable=False)

    district: Mapped[schemas.District] = mapped_column(PydanticType(schemas.District), nullable=False)
    clinic: Mapped[schemas.Clinic] = mapped_column(PydanticType(schemas.Clinic), nullable=False)
    speciality: Mapped[schemas.Speciality] = mapped_column(PydanticType(schemas.Speciality), nullable=False)
    doctor: Mapped[schemas.Doctor] = mapped_column(PydanticType(schemas.Doctor), nullable=False)
