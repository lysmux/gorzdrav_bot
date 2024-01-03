from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage, StorageKey

from src.database.models import TrackingModel
from src.gorzdrav_api.schemas import Appointment

APPOINTMENTS_KEY = "appointments"


class CheckerStorageProxy:
    def __init__(
            self,
            storage: BaseStorage,
            bot: Bot,
            tracking: TrackingModel
    ) -> None:
        self.storage = storage
        self.bot = bot
        self.tracking = tracking

    async def get_appointments(self) -> list[Appointment]:
        data = await self.storage.get_data(
            key=self._storage_key()
        )

        return data.get(APPOINTMENTS_KEY)

    async def set_appointments(self, appointments: list[Appointment]) -> None:
        await self.storage.set_data(
            key=self._storage_key(),
            data={APPOINTMENTS_KEY: appointments}
        )

    async def remove(self) -> None:
        await self.storage.set_data(
            key=self._storage_key(),
            data={}
        )

    def _storage_key(self) -> StorageKey:
        return StorageKey(
            bot_id=self.bot.id,
            chat_id=self.tracking.user.tg_id,
            user_id=self.tracking.user.tg_id,
            destiny=f"checker:{self.tracking.id}"
        )
