import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiogram_dialog import setup_dialogs
from aiogram_dialog.widgets.text.jinja import JINJA_ENV_FIELD
from aiohttp import web
from cashews import cache
from redis.asyncio import Redis

from bot.logic import general, gorzdrav
from bot.middlewares.database import DatabaseMiddleware
from bot.middlewares.gorzdrav_api import GorZdravAPIMiddleware
from bot.services.appointments_checker import AppointmentsChecker
from bot.services.set_bot_commands import set_bot_commands
from bot.utils.redis_storage import RedisPickleStorage
from bot.utils.template_engine import env as jinja_env
from config import Settings
from database.database import create_db_pool

logger = logging.getLogger("main")


async def run(settings: Settings):
    if settings.use_redis:
        logger.debug("Using Redis for cache")
        redis = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            password=settings.redis.password
        )
        storage = RedisPickleStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))
        cache.setup(
            f"redis://{settings.redis.host}:{settings.redis.port}",
            password=settings.redis.password,
            socket_connect_timeout=0.1,
            retry_on_timeout=True,
            client_side=True
        )
    else:
        logger.debug("Using Memory for cache")
        storage = MemoryStorage()
        cache.setup("mem://")

    database_pool = await create_db_pool(settings)

    bot = Bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        general.router,
        gorzdrav.router
    )

    dp.message.middleware(DatabaseMiddleware(database_pool))
    dp.callback_query.middleware(DatabaseMiddleware(database_pool))

    dp.message.middleware(GorZdravAPIMiddleware())
    dp.callback_query.middleware(GorZdravAPIMiddleware())

    manager_factory = setup_dialogs(dp)
    setattr(bot, JINJA_ENV_FIELD, jinja_env)

    appointments_checker = AppointmentsChecker(
        bot=bot,
        manager_factory=manager_factory,
        storage=dp.storage,
        database_pool=database_pool,
        check_every=settings.check_every,
    )

    await set_bot_commands(bot)

    async with asyncio.TaskGroup() as tg:
        if settings.use_webhook:
            tg.create_task(run_bot_as_webhook(bot=bot, dispatcher=dp, settings=settings))
        else:
            tg.create_task(run_bot_as_pooling(bot=bot, dispatcher=dp))

        tg.create_task(appointments_checker.run())


async def run_bot_as_pooling(bot: Bot, dispatcher: Dispatcher):
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


async def run_bot_as_webhook(
        bot: Bot,
        dispatcher: Dispatcher,
        settings: Settings
):
    app = web.Application()
    runner = web.AppRunner(app)

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=settings.webhook.secret
    )
    webhook_requests_handler.register(app, path=settings.webhook.path)
    setup_application(app, dispatcher, bot=bot)

    await bot.set_webhook(
        url=settings.webhook.url,
        secret_token=settings.webhook.secret,
        drop_pending_updates=True
    )

    await runner.setup()
    webhook_site = web.TCPSite(
        runner,
        host=settings.webhook.app_host,
        port=settings.webhook.app_port
    )

    logger.info(f"WebHook server is running on {settings.webhook.app_host}:{settings.webhook.app_port}")
    try:
        await webhook_site.start()
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


def main():
    settings = Settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        logger.info("GorZdrav bot is running")
        asyncio.run(run(settings=settings))
    except (KeyboardInterrupt, SystemExit):
        logger.info("GorZdrav bot stopped")


if __name__ == "__main__":
    main()
