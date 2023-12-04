from aiogram import Router

from src.bot.logic.gorzdrav.dialogs import manage_tracking, add_tracking, appointment, new_appointment

router = Router()

router.include_routers(
    appointment.dialog,
    add_tracking.dialog,
    manage_tracking.dialog,
    new_appointment.dialog
)
