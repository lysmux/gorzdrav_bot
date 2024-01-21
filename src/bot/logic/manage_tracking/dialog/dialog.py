from aiogram_dialog import Dialog

from .windows import (
    list, action,
    status, deleted
)

DIALOG_NAME = "manage_tracking"

dialog = Dialog(
    list.window,
    action.window,
    status.window,
    deleted.window,
    name=DIALOG_NAME
)
