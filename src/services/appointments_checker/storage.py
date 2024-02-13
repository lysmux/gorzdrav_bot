from aiogram.fsm.storage.base import BaseStorage, StorageKey

APPOINTMENTS_KEY = "appointments"

type AppointmentsData = dict[int, int]


class StorageProxy:
    def __init__(
            self,
            bot_id: int,
            user_id: int,
            storage: BaseStorage
    ) -> None:
        self.bot_id = bot_id
        self.user_id = user_id
        self.storage = storage

    async def get_data(self) -> AppointmentsData:
        data = await self.storage.get_data(
            key=self._storage_key()
        )

        return data.get(APPOINTMENTS_KEY, {})

    async def set_data(self, data: AppointmentsData) -> None:
        await self.storage.set_data(
            key=self._storage_key(),
            data={APPOINTMENTS_KEY: data}
        )

    async def clear(self) -> None:
        await self.storage.set_data(
            key=self._storage_key(),
            data={}
        )

    def _storage_key(self) -> StorageKey:
        return StorageKey(
            bot_id=self.bot_id,
            chat_id=self.user_id,
            user_id=self.user_id,
            destiny="checker"
        )
