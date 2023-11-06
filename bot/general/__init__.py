from aiogram import Router

from bot.general import handlers, dialogs

router = Router()

router.include_routers(
    handlers.router,
    dialogs.router
)
