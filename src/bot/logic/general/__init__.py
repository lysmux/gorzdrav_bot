from aiogram import Router, F
from aiogram.filters import Command, or_f

from . import handlers, dialogs

ROUTER_NAME = "general"


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.message.filter(
        or_f(
            Command(commands=["start", "help"]),
            ~F.text.startswith("/")
        )
    )

    router.include_routers(
        handlers.router,
        *dialogs.routers
    )

    return router
