import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot import common, gorzdrav
from bot.middlewares.database import DatabaseMiddleware
from bot.utils.appointments_checker import AppointmentsChecker
from bot.utils.set_bot_commands import set_bot_commands
from config import Settings
from database.database import create_db_pool
from misc.redis_storage import Redis
from misc.redis_storage import RedisPickleStorage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    settings = Settings()

    if settings.use_redis:
        redis = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            password=settings.redis.password
        )
        storage = RedisPickleStorage(redis)
    else:
        redis = None
        storage = MemoryStorage()

    database_pool = await create_db_pool(
        host=settings.db.host,
        port=settings.db.port,
        user=settings.db.user,
        password=settings.db.password,
        database=settings.db.database,
    )

    bot = Bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        gorzdrav.router,
        common.router,
    )
    dp.message.middleware(DatabaseMiddleware(database_pool))
    dp.callback_query.middleware(DatabaseMiddleware(database_pool))

    appointments_checker = AppointmentsChecker(
        bot=bot,
        dispatcher=dp,
        database_pool=database_pool,
        check_every=settings.check_every,
        redis=redis
    )

    await set_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(dp.start_polling(bot))
            tg.create_task(appointments_checker.run())
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        logger.info("Starting bot")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
