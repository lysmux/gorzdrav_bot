from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database.repositories.tracking import TrackingRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, database_pool):
        self.database_pool = database_pool

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                       ) -> Any:
        async with self.database_pool() as session:
            async with session.begin():
                data["repository"] = TrackingRepo(session)
                return await handler(event, data)
