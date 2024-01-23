from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .tracking import TrackingModel


class UserModel(BaseModel):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)

    tracking: Mapped[list["TrackingModel"]] = relationship(
        back_populates="user",
        lazy="selectin",
        uselist=True,
        order_by="tracking.clinic"
    )
