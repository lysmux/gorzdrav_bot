from aiogram import Router

from bot.gorzdrav.dialogs import (
    appointment,
    add_tracking,
    manage_tracking,
    new_appointment
)

router = Router()

router.include_routers(
    appointment.dialog,
    add_tracking.dialog,
    manage_tracking.dialog,
    new_appointment.dialog
)
