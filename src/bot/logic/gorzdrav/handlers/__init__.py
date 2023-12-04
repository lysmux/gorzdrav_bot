from aiogram import Router

from src.bot.logic.gorzdrav.handlers import errors
from src.bot.logic.gorzdrav.handlers import common

router = Router()
router.include_routers(
    common.router,
    errors.router
)
