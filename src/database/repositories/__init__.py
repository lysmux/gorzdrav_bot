from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import AbstractRepo
from .tracking import TrackingRepo
from .user import UserRepo


class Repository:
    def __init__(self, session: AsyncSession):
        self.tracking = TrackingRepo(session=session)
        self.user = UserRepo(session=session)
