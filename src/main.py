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
from bot.services.set_bot_commands import set_bot_commands
from bot.utils.redis_storage import RedisPickleStorage
from bot.utils.template_engine import env as jinja_env
from config import settings
from src.bot.services.appointments_checker import AppointmentsChecker
from src.bot.structures.context import ContextData
from src.database.database import get_engine

logger = logging.getLogger("main")


def get_storage():
    if settings.use_redis:
        logger.info("Using Redis for cache")
        redis = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            password=settings.redis.password
        )
        storage = RedisPickleStorage(
            redis,
            key_builder=DefaultKeyBuilder(with_destiny=True)
        )
        cache.setup(
            f"redis://{settings.redis.host}:{settings.redis.port}",
            password=settings.redis.password,
            socket_connect_timeout=0.1,
            retry_on_timeout=True,
            client_side=True
        )
    else:
        logger.info("Using Memory for cache")
        storage = MemoryStorage()
        cache.setup("mem://")

    return storage


async def run_bot():
    storage = get_storage()
    engine = get_engine()

    # setup dispatcher
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        general.get_router(),
        gorzdrav.get_router()
    )

    # setup bot
    bot = Bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    setattr(bot, JINJA_ENV_FIELD, jinja_env)
    await set_bot_commands(bot)

    # setup aiogram dialogs
    aiod_manager_factory = setup_dialogs(dp)

    # setup appointments checker
    appointments_checker = AppointmentsChecker(
        bot=bot,
        manager_factory=aiod_manager_factory,
        storage=storage,
        db_engine=engine,
        check_every=settings.check_every,
    )

    # run
    async with asyncio.TaskGroup() as tg:
        if settings.use_webhook:
            task = run_as_webhook(
                bot=bot,
                dispatcher=dp,
                context_data=ContextData(engine=engine)
            )
        else:
            task = run_as_pooling(
                bot=bot,
                dispatcher=dp,
                context_data=ContextData(engine=engine)
            )

        tg.create_task(task)
        tg.create_task(appointments_checker.run())


async def run_as_pooling(
        bot: Bot,
        dispatcher: Dispatcher,
        context_data: ContextData
):
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, **context_data)


async def run_as_webhook(
        bot: Bot,
        dispatcher: Dispatcher,
        context_data: ContextData
):
    app = web.Application()
    runner = web.AppRunner(app)

    # setup aiohttp server
    await runner.setup()
    webhook_site = web.TCPSite(
        runner,
        host=settings.webhook.app_host,
        port=settings.webhook.app_port
    )

    # setup requests handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=settings.webhook.secret,
        **context_data
    )
    webhook_requests_handler.register(app, path=settings.webhook.path)
    setup_application(app, dispatcher)

    await bot.set_webhook(
        url=settings.webhook.url,
        secret_token=settings.webhook.secret,
        drop_pending_updates=True
    )

    logger.info(f"WebHook server is running on {settings.webhook.app_host}:{settings.webhook.app_port}")
    try:
        await webhook_site.start()
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


def main():
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        logger.info("GorZdrav bot is running")
        asyncio.run(run_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info("GorZdrav bot stopped")


if __name__ == "__main__":
    main()
