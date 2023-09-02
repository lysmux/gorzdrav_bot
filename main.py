import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import Config
from handlers import common, gorzdrav
from services.set_bot_commands import set_bot_commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot")
    config = Config.load_config("bot.ini")

    if config.bot.use_redis:
        storage = RedisStorage(Redis())
    else:
        storage = MemoryStorage()
    # pool = await create_pool(
    #     host=config.db.host,
    #     port=config.db.port,
    #     user=config.db.user,
    #     password=config.db.password,
    #     database=config.db.database,
    # )

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        gorzdrav.router,
        common.router,
    )

    await set_bot_commands(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
