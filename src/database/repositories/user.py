from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserModel
from src.database.repositories import AbstractRepo


class UserRepo(AbstractRepo[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_type=UserModel)

    async def new(self, tg_id: int) -> UserModel:
        user = UserModel(tg_id=tg_id)
        self.session.add(user)

        return user
