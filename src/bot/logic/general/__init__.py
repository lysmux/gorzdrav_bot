from aiogram import Router, F
from aiogram.filters import Command, or_f

from . import handlers, dialogs

router = Router()

router.message.filter(
    or_f(
        Command(commands=["start", "help"]),
        ~F.text.startswith("/")
    )
)

router.include_routers(
    handlers.router,
    dialogs.router
)
