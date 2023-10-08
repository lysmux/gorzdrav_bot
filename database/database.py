import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database.models.base import Base
from database.models.profile import Profile
from database.models.tracking import Tracking
from gorzdrav_api.schemas import District, Doctor, Speciality, Clinic


async def create_db_pool(host: str, user: str, password: str, database: str):
    database_url = f"postgresql+asyncpg://{user}:{password}@{host}/{database}"

    engine = create_async_engine(database_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    return async_session


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_profile(
            self,
            tg_user_id: int,
            last_name: str,
            first_name: str,
            middle_name: str,
            birthdate: datetime.date
    ):
        profile = Profile(
            tg_user_id=tg_user_id,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birthdate=birthdate
        )
        self.session.add(profile)
        await self.session.commit()

    async def delete_profile(self, profile: Profile):
        await self.session.delete(profile)
        await self.session.commit()

    async def get_user_profiles(self, tg_user_id: int):
        stmt = select(Profile).where(Profile.tg_user_id == tg_user_id)
        result = await self.session.scalars(stmt)
        return result

    async def add_tracking(
            self,
            tg_user_id: int,
            district: District,
            clinic: Clinic,
            speciality: Speciality,
            doctor: Doctor,
            hours: list[int]

    ):
        tracking = Tracking(
            tg_user_id=tg_user_id,
            district=district,
            clinic=clinic,
            speciality=speciality,
            doctor=doctor,
            hours=hours
        )
        self.session.add(tracking)
        await self.session.commit()

    async def delete_tracking(self, tracking_id: int):
        stmt = delete(Tracking).where(Tracking.id == tracking_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_user_tracking(self, tg_user_id: int):
        stmt = select(Tracking).where(Tracking.tg_user_id == tg_user_id)
        result = await self.session.scalars(stmt)
        return result
