from aiogram_dialog import Dialog

from bot.gorzdrav.dialogs.appointment.windows import (
    districts,
    clinics,
    doctors,
    specialities,
    appointments,
)

dialog = Dialog(
    districts.window,
    clinics.window,
    specialities.window,
    doctors.window,
    appointments.window
)
