from aiogram import Router, F
from aiogram.filters import or_f, Command

from . import handlers, dialog

ROUTER_NAME = "manage_tracking"
COMMANDS = (
    "tracking"
)


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.message.filter(or_f(
        Command(commands=COMMANDS),
        ~F.text.startswith("/")
    ))

    router.include_routers(
        handlers.router,
        dialog.dialog
    )

    return router
