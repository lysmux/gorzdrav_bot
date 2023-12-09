import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from config import settings

logger = logging.getLogger("database")


def get_engine() -> AsyncEngine:
    engine = create_async_engine(settings.db.url, pool_pre_ping=True)

    logger.info(f"Database <{settings.db.database}> on "
                f"{settings.db.host}:{settings.db.port}")

    return engine
