from aiogram_dialog import Dialog

from src.bot.logic.gorzdrav.dialogs.appointment.windows import (
    appointments,
)
from src.bot.logic.gorzdrav.dialogs.appointment.windows import clinics
from src.bot.logic.gorzdrav.dialogs.appointment.windows import districts, specialities, doctors

dialog = Dialog(
    districts.window,
    clinics.window,
    specialities.window,
    doctors.window,
    appointments.window
)
