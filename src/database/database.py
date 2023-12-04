import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .models.base import Base
from src.config import Settings

logger = logging.getLogger("database")


async def create_db_pool(settings: Settings):
    database_url = (f"postgresql+asyncpg://"
                    f"{settings.db.user}:{settings.db.password}"
                    f"@{settings.db.host}:{settings.db.port}"
                    f"/{settings.db.database}")

    engine = create_async_engine(database_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    logger.info(f"Successful connection to the {settings.db.database} database on "
                f"{settings.db.host}:{settings.db.port}")
    return async_session
