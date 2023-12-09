from aiogram_dialog import Dialog

from . import window

DIALOG_NAME = "new_appointments_dialog"

dialog = Dialog(
    window.window,
    name=DIALOG_NAME
)
