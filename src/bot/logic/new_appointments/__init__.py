from aiogram import Router

from . import dialog

ROUTER_NAME = "new_appointments"


def get_router() -> Router:
    router = Router(name=ROUTER_NAME)

    router.include_routers(
        dialog.dialog
    )

    return router
