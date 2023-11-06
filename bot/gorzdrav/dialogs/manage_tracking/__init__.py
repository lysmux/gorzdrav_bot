from aiogram_dialog import Dialog

from bot.gorzdrav.dialogs.manage_tracking.windows import (
    list,
    deleted,
    action,
    status
)

dialog = Dialog(
    list.window,
    action.window,
    status.window,
    deleted.window,
)
