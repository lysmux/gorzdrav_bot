from aiogram import Router, F
from aiogram.filters import or_f, Command

from src.config import settings
from . import handlers, dialog

ROUTER_NAME = "admin"
COMMANDS = (
    "admin"
)


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.message.filter(
        or_f(
            Command(commands=COMMANDS),
            ~F.text.startswith("/")
        ),
        F.from_user.id.in_(settings.admins)
    )
    router.callback_query.filter(
        F.from_user.id.in_(settings.admins)
    )

    router.include_routers(
        handlers.router,
        dialog.dialog
    )

    return router
