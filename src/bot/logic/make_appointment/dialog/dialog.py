from aiogram_dialog import Dialog

from .windows import (
    district,
    clinic,
    speciality,
    doctor,
    appointment,
    tracking_add,
    tracking_added
)

DIALOG_NAME = "make_appointment"

dialog = Dialog(
    district.window,
    clinic.window,
    speciality.window,
    doctor.window,
    appointment.window,
    tracking_add.window,
    tracking_added.window,
    name=DIALOG_NAME
)
