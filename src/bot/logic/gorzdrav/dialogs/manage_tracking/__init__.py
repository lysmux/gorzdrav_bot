from aiogram_dialog import Dialog

from src.bot.logic.gorzdrav.dialogs.manage_tracking.windows import (
    list
)
from src.bot.logic.gorzdrav.dialogs.manage_tracking.windows import deleted, status, action

dialog = Dialog(
    list.window,
    action.window,
    status.window,
    deleted.window,
)
