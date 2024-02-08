from aiogram import Router

from . import gorzdrav, dialog, general

ROUTER_NAME = "errors"


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.include_routers(
        general.router,
        gorzdrav.router,
        dialog.router
    )

    return router
