import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings

logger = logging.getLogger("database")


async def create_db_pool() -> async_sessionmaker:
    engine = create_async_engine(settings.db.url, pool_pre_ping=True)
    session_maker = async_sessionmaker(engine)

    logger.info(f"Successful connection to the {settings.db.database} database on "
                f"{settings.db.host}:{settings.db.port}")

    return session_maker
