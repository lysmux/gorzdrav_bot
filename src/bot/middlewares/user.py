from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.bot.structures import TransferStruct
from src.database.models import UserModel


class UserMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: TransferStruct
                       ) -> Any:
        repository = data["repository"]

        user = await repository.user.get(clause=UserModel.tg_id == event.from_user.id)
        if not user:
            user = await repository.user.new(tg_id=event.from_user.id)

        data["user"] = user
        return await handler(event, data)
