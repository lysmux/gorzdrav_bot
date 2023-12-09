import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from cashews import cache
from redis.asyncio import Redis

from bot.logic import routers
from bot.middlewares import GorZdravAPIMiddleware, DatabaseMiddleware
from bot.structures import TransferStruct
from bot.utils.redis_storage import RedisPickleStorage
from config import settings

logger = logging.getLogger("bot")


def get_storage() -> BaseStorage:
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


def get_dispatcher() -> Dispatcher:
    storage = get_storage()
    dispatcher = Dispatcher(storage=storage)

    # setup routers
    dispatcher.include_routers(*routers)

    # setup middlewares
    database_mid = DatabaseMiddleware()
    dispatcher.message.middleware(database_mid)
    dispatcher.callback_query.middleware(database_mid)

    gorzdrav_api_mid = GorZdravAPIMiddleware()
    dispatcher.message.middleware(gorzdrav_api_mid)
    dispatcher.callback_query.middleware(gorzdrav_api_mid)

    return dispatcher


async def run_as_pooling(
        bot: Bot,
        dispatcher: Dispatcher,
        transfer_data: TransferStruct
) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, **transfer_data)


async def run_as_webhook(
        bot: Bot,
        dispatcher: Dispatcher,
        transfer_data: TransferStruct
) -> None:
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
        **transfer_data
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
