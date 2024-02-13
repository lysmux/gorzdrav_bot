from aiogram import Router, F
from aiogram.filters import or_f, Command, MagicData

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
        MagicData(F["user_is_admin"].is_(True))
    )
    router.callback_query.filter(
        MagicData(F["user_is_admin"].is_(True))
    )

    router.include_routers(
        handlers.router,
        dialog.dialog
    )

    return router
