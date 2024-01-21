from aiogram_dialog import Dialog

from .windows import menu

DIALOG_NAME = "general"

dialog = Dialog(
    menu.window,
    name=DIALOG_NAME
)
