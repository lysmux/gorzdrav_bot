import asyncio
import logging
from datetime import timedelta

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from cashews import cache
from redis.asyncio import Redis

from src.bot.logic import handlers, dialogs, errors
from src.bot.middlewares import (
    GorZdravAPIMiddleware,
    DatabaseMiddleware,
    UserMiddleware
)
from src.bot.structures import TransferStruct
from src.bot.utils.redis_storage import RedisPickleStorage
from src.settings import Settings, WebhookSettings

logger = logging.getLogger(__name__)


def get_storage(settings: Settings) -> BaseStorage:
    if settings.use_redis:
        logger.info("Using Redis for cache")
        ttl = timedelta(weeks=1)
        redis = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            password=settings.redis.password
        )
        storage = RedisPickleStorage(
            redis,
            key_builder=DefaultKeyBuilder(with_destiny=True),
            data_ttl=ttl,
            state_ttl=ttl
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


def get_dispatcher(
        settings: Settings,
        transfer_data: TransferStruct
) -> Dispatcher:
    storage = get_storage(settings=settings)
    dispatcher = Dispatcher(storage=storage, **transfer_data)

    # setup routers
    dispatcher.include_routers(
        *errors.routers,
        *handlers.routers,
        *dialogs.routers,
    )

    # setup middlewares
    database_mid = DatabaseMiddleware()
    user_mid = UserMiddleware(admins=settings.admins)
    gorzdrav_api_mid = GorZdravAPIMiddleware()

    for mid in (
            gorzdrav_api_mid,
    ):
        dispatcher.message.middleware(mid)
        dispatcher.callback_query.middleware(mid)
    for mid in (
            database_mid,
            user_mid
    ):
        dispatcher.message.outer_middleware(mid)
        dispatcher.callback_query.outer_middleware(mid)

    return dispatcher


async def run_as_pooling(
        bot: Bot,
        dispatcher: Dispatcher
) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


async def run_as_webhook(
        bot: Bot,
        dispatcher: Dispatcher,
        webhook_settings: WebhookSettings
) -> None:
    app = web.Application()
    runner = web.AppRunner(app)

    # setup requests handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=webhook_settings.secret
    )
    webhook_requests_handler.register(app, path=webhook_settings.path)
    setup_application(app, dispatcher)

    # setup aiohttp server
    await runner.setup()
    webhook_site = web.TCPSite(
        runner,
        host=webhook_settings.app_host,
        port=webhook_settings.app_port
    )

    # set webhook url
    await bot.set_webhook(
        url=webhook_settings.url,
        secret_token=webhook_settings.secret,
        drop_pending_updates=True
    )

    logger.info(f"WebHook server is running on "
                f"{webhook_settings.app_host}:{webhook_settings.app_port}")
    try:
        await webhook_site.start()
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()
