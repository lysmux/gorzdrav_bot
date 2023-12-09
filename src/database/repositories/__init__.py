from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import AbstractRepo
from .tracking import TrackingRepo


class Repository:
    def __init__(self, session: AsyncSession):
        self.tracking = TrackingRepo(session=session)
