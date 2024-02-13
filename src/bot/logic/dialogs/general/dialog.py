from aiogram_dialog import Dialog

from .windows import menu

DIALOG_NAME = "general_dialog"

dialog = Dialog(
    menu.window,
    name=DIALOG_NAME
)
