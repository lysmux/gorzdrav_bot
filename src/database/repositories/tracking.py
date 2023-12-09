from sqlalchemy.ext.asyncio import AsyncSession

from gorzdrav_api import schemas
from . import AbstractRepo
from ..models import TrackingModel


class TrackingRepo(AbstractRepo[TrackingModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_type=TrackingModel)

    async def add(
            self,
            tg_user_id: int,
            district: schemas.District,
            clinic: schemas.Clinic,
            speciality: schemas.Speciality,
            doctor: schemas.Doctor,
            time_ranges: list[list[int]]

    ) -> None:
        tracking = TrackingModel(
            tg_user_id=tg_user_id,
            district=district,
            clinic=clinic,
            speciality=speciality,
            doctor=doctor,
            time_ranges=time_ranges
        )
        self.session.add(tracking)
