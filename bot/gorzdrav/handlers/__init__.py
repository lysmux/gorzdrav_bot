from aiogram import Router

from bot.gorzdrav.handlers import errors, search_doctor, make_appointment

router = Router()
router.include_routers(search_doctor.router, make_appointment.router, errors.router)
