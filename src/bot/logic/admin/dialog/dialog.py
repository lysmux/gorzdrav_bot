from aiogram_dialog import Dialog

from .windows import action, statistics

DIALOG_NAME = "admin"

dialog = Dialog(
    action.window,
    statistics.window,
    name=DIALOG_NAME
)
