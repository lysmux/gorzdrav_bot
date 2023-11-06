from aiogram import Router

from bot.gorzdrav.handlers import common, errors

router = Router()
router.include_routers(
    common.router,
    errors.router
)
