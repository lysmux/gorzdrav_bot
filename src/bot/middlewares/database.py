from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.context import ContextData
from src.database.repositories import Repository


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: ContextData
                       ) -> Any:
        async with AsyncSession(bind=data["engine"]) as session:
            async with session.begin():
                data["repository"] = Repository(session)
                return await handler(event, data)
