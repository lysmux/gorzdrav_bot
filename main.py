import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from redis.asyncio import Redis

from bot import common, gorzdrav
from bot.middlewares.database import DatabaseMiddleware
from bot.utils.appointments_checker import AppointmentsChecker
from bot.utils.redis_storage import RedisPickleStorage
from bot.utils.set_bot_commands import set_bot_commands
from config import Settings
from database.database import create_db_pool

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

    async with asyncio.TaskGroup() as tg:
        if settings.use_webhook:
            tg.create_task(run_as_webhook(bot=bot, dispatcher=dp, settings=settings))
        else:
            tg.create_task(run_as_pooling(bot=bot, dispatcher=dp))

        tg.create_task(appointments_checker.run())


async def run_as_pooling(bot: Bot, dispatcher: Dispatcher):
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


async def run_as_webhook(bot: Bot, dispatcher: Dispatcher, settings: Settings):
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()

    webhook_site = web.TCPSite(
        runner,
        host=settings.webhook.server_host,
        port=settings.webhook.server_port
    )

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=settings.webhook.secret
    )
    webhook_requests_handler.register(app, path=settings.webhook.path)
    setup_application(app, dispatcher, bot=bot)

    await bot.set_webhook(
        url=settings.webhook.url + settings.webhook.path,
        secret_token=settings.webhook.secret,
        drop_pending_updates=True
    )
    await webhook_site.start()


if __name__ == "__main__":
    try:
        logger.info("Starting bot")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
