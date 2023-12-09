from aiogram import Router, F
from aiogram.filters import Command, or_f

from src.bot.middlewares.database import DatabaseMiddleware
from src.bot.middlewares.gorzdrav_api import GorZdravAPIMiddleware
from . import handlers, dialogs

ROUTER_NAME = "gorzdrav"


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.message.filter(or_f(
        Command(commands=["appointment", "tracking"]),
        ~F.text.startswith("/")
    ))

    router.include_routers(
        *handlers.routers,
        *dialogs.routers
    )

    router.message.middleware(DatabaseMiddleware())
    router.callback_query.middleware(DatabaseMiddleware())

    router.message.middleware(GorZdravAPIMiddleware())
    router.callback_query.middleware(GorZdravAPIMiddleware())

    return router
