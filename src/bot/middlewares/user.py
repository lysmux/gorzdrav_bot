from typing import Callable, Dict, Awaitable, Any, Sequence

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, ErrorEvent

from src.bot.structures import TransferStruct
from src.database.models import UserModel

type Event = Message | CallbackQuery | ErrorEvent


class UserMiddleware(BaseMiddleware):
    def __init__(self, admins: Sequence[int]):
        self.admins = admins

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Event,
                       data: TransferStruct
                       ) -> Any:
        repository = data["repository"]

        user = await repository.user.get(clause=UserModel.tg_id == event.from_user.id)
        if not user:
            user = await repository.user.new(tg_id=event.from_user.id)

        data["user"] = user
        data["user_is_admin"] = event.from_user.id in self.admins
        return await handler(event, data)
