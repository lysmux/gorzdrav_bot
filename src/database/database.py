import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.settings import DatabaseSettings

logger = logging.getLogger(__name__)


def get_engine(db_settings: DatabaseSettings) -> AsyncEngine:
    engine = create_async_engine(db_settings.url, pool_pre_ping=True)

    logger.info(f"Database <{db_settings.database}> on "
                f"{db_settings.host}:{db_settings.port}")

    return engine
