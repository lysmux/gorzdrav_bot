from aiogram import Router

from bot.gorzdrav import handlers, dialogs

router = Router()

router.include_routers(
    handlers.router,
    dialogs.router
)
