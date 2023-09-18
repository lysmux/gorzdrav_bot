from aiogram import Router

from bot.gorzdrav.handlers import errors, search_doctor

router = Router()
router.include_routers(search_doctor.router, errors.router)
