from aiogram import Router, F
from aiogram.filters import Command, or_f

from . import handlers, dialog

ROUTER_NAME = "general"
COMMANDS = (
    "start",
    "help"
)


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.message.filter(
        or_f(
            Command(commands=COMMANDS),
            ~F.text.startswith("/")
        )
    )

    router.include_routers(
        handlers.router,
        dialog.dialog
    )

    return router
