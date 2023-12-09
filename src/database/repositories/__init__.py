from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories.tracking import TrackingRepo


class Repository:
    def __init__(self, session: AsyncSession):
        self.tracking = TrackingRepo(session=session)
