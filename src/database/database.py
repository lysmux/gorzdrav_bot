import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings import DatabaseSettings

logger = logging.getLogger(__name__)


def get_session_maker(db_settings: DatabaseSettings) -> async_sessionmaker:
    engine = create_async_engine(db_settings.url, pool_pre_ping=True)
    session_maker = async_sessionmaker(bind=engine)

    logger.info(f"Database <{db_settings.database}> on "
                f"{db_settings.host}:{db_settings.port}")

    return session_maker
