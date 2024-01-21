from aiogram import Router

from . import gorzdrav

ROUTER_NAME = "errors"


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.include_routers(
        gorzdrav.router
    )

    return router
