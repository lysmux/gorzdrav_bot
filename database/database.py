import logging

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import Settings
from database.models.base import Base
from database.models.tracking import Tracking
from gorzdrav_api.schemas import District, Doctor, Speciality, Clinic

logger = logging.getLogger("database")


async def create_db_pool(settings: Settings):
    database_url = (f"postgresql+asyncpg://"
                    f"{settings.db.user}:{settings.db.password}"
                    f"@{settings.db.host}:{settings.db.port}"
                    f"/{settings.db.database}")

    engine = create_async_engine(database_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    logger.info(f"Successful connection to the {settings.db.database} database on "
                f"{settings.db.host}:{settings.db.port}")
    return async_session


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_tracking(
            self,
            tg_user_id: int,
            district: District,
            clinic: Clinic,
            speciality: Speciality,
            doctor: Doctor,
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
        await self.session.commit()

        logger.debug(f"Added tracking with ID {tracking.id}")

    async def delete_tracking(self, tracking_id: int):
        stmt = delete(Tracking).where(Tracking.id == tracking_id)
        await self.session.execute(stmt)
        await self.session.commit()

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
