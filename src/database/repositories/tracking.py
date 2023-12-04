import logging

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.tracking import Tracking
from src.gorzdrav_api import schemas

logger = logging.getLogger("database")


class TrackingRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_tracking(
            self,
            tg_user_id: int,
            district: schemas.District,
            clinic: schemas.Clinic,
            speciality: schemas.Speciality,
            doctor: schemas.Doctor,
            time_ranges: list[list[int]]

    ):
        tracking = Tracking(
            tg_user_id=tg_user_id,
            district=district,
            clinic=clinic,
            speciality=speciality,
            doctor=doctor,
            time_ranges=time_ranges
        )
        self.session.add(tracking)

        logger.debug(f"Added tracking with ID {tracking.id}")

    async def delete_tracking(self, tracking_id: int):
        stmt = delete(Tracking).where(Tracking.id == tracking_id)
        await self.session.execute(stmt)

        logger.debug(f"Removed tracking with ID {tracking_id}")

    async def get_user_tracking(self, tg_user_id: int):
        stmt = select(Tracking).where(Tracking.tg_user_id == tg_user_id)
        result = await self.session.scalars(stmt)

        logger.debug(f"All user ({tg_user_id=}) tracking received")

        return result

    async def get_all_tracking(self):
        stmt = select(Tracking)
        result = await self.session.scalars(stmt)

        logger.debug(f"All tracking received")

        return result
