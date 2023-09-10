from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from gorzdrav_api.api import GorZdravAPI


class GorZdravAPIMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                       ) -> Any:
        async with GorZdravAPI() as session:
            data["gorzdrav_api"] = session
            return await handler(event, data)
