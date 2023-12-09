from aiogram_dialog import Dialog

from .windows import (
    districts,
    clinics,
    specialities,
    doctors,
    appointments,
    tracking_add,
    tracking_added
)

DIALOG_NAME = "make_appointment_dialog"

dialog = Dialog(
    districts.window,
    clinics.window,
    specialities.window,
    doctors.window,
    appointments.window,
    tracking_add.window,
    tracking_added.window,
    name=DIALOG_NAME
)
