from aiogram import Router, F
from aiogram.filters import or_f, Command

from bot.gorzdrav import handlers, dialogs

router = Router()

router.message.filter(or_f(
    Command(commands=["appointment", "tracking"]),
    ~F.text.startswith("/")
))

router.include_routers(
    handlers.router,
    dialogs.router
)
