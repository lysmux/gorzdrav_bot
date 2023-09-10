from aiogram import Router

from bot.gorzdrav.handlers import gorzdrav, errors

router = Router()
router.include_routers(gorzdrav.router, errors.router)
