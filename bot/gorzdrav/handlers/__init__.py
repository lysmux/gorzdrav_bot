from aiogram import Router

from bot.gorzdrav.handlers import errors, search_doctor, add_tracking, manage_tracking

router = Router()
router.include_routers(search_doctor.router,
                       add_tracking.router,
                       manage_tracking.router,
                       errors.router)
