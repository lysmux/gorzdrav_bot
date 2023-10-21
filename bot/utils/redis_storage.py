import pickle
from typing import Any, cast

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from aiogram.fsm.storage.redis import DefaultKeyBuilder, KeyBuilder, RedisEventIsolation
from redis import ConnectionPool
from redis.asyncio import Redis
from redis.typing import ExpiryT


class RedisPickleStorage(BaseStorage):
    """
    Redis storage with pickle encode
    """

    def __init__(
            self,
            redis: Redis,
            key_builder: KeyBuilder | None = None,
            state_ttl: ExpiryT | None = None,
            data_ttl: ExpiryT | None = None,
    ) -> None:
        """
        :param redis: Instance of Redis connection
        :param key_builder: builder that helps to convert contextual key to string
        :param state_ttl: TTL for state records
        :param data_ttl: TTL for data records
        """
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.redis = redis
        self.key_builder = key_builder
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl

    @classmethod
    def from_url(
            cls,
            url: str,
            connection_kwargs: dict[str, Any] | None = None,
            **kwargs: Any
    ) -> "RedisPickleStorage":
        """
        Create an instance of :class:`RedisStorage` with specifying the connection string

        :param url: for example :code:`redis://user:password@host:port/db`
        :param connection_kwargs: see :code:`redis` docs
        :param kwargs: arguments to be passed to :class:`RedisStorage`
        :return: an instance of :class:`RedisStorage`
        """
        if connection_kwargs is None:
            connection_kwargs = {}
        pool = ConnectionPool.from_url(url, **connection_kwargs)
        redis = Redis(connection_pool=pool)
        return cls(redis=redis, **kwargs)

    def create_isolation(self, **kwargs: Any) -> "RedisEventIsolation":
        return RedisEventIsolation(redis=self.redis, key_builder=self.key_builder, **kwargs)

    async def close(self) -> None:
        await self.redis.close()

    async def set_state(
            self,
            key: StorageKey,
            state: StateType = None,
    ) -> None:
        redis_key = self.key_builder.build(key, "state")
        if state is None:
            await self.redis.delete(redis_key)
        else:
            await self.redis.set(
                redis_key,
                cast(str, state.state if isinstance(state, State) else state),
                ex=self.state_ttl,
            )

    async def get_state(
            self,
            key: StorageKey,
    ) -> str | None:
        redis_key = self.key_builder.build(key, "state")
        value = await self.redis.get(redis_key)
        if isinstance(value, bytes):
            return value.decode("utf-8")
        return cast(str | None, value)

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
        return cast(dict[str, Any], pickle.loads(value))
