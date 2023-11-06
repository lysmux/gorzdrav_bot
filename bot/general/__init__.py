from aiogram import Router
from aiogram.filters import Command

from bot.general import handlers, dialogs

router = Router()

router.message.filter(
    Command(commands=["start", "help"])
)

router.include_routers(
    handlers.router,
    dialogs.router
)
