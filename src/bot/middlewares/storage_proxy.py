from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.bot.structures import TransferStruct
from src.services.appointments_checker import StorageProxy


class StorageProxyMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: TransferStruct
                       ) -> Any:
        storage_proxy = StorageProxy(
            bot_id=data["bot"].id,
            user_id=data["event_from_user"].id,
            storage=data["fsm_storage"]
        )
        data["storage_proxy"] = storage_proxy
        return await handler(event, data)
