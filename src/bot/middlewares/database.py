from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.bot.structures import TransferStruct
from src.database import Repository


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: TransferStruct
                       ) -> Any:
        session_maker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                data["repository"] = Repository(session)
                return await handler(event, data)
