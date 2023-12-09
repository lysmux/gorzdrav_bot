import pickle
from typing import Any

from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage


class RedisPickleStorage(RedisStorage):
    async def set_data(
            self,
            key: StorageKey,
            data: dict[str, Any],
    ) -> None:
        redis_key = self.key_builder.build(key, "data")
        if not data:
            await self.redis.delete(redis_key)
            return
        await self.redis.set(
            redis_key,
            pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL),
            ex=self.data_ttl,
        )

    async def get_data(
            self,
            key: StorageKey,
    ) -> dict[str, Any]:
        redis_key = self.key_builder.build(key, "data")
        value = await self.redis.get(redis_key)
        if value is None:
            return {}
        return pickle.loads(value)
