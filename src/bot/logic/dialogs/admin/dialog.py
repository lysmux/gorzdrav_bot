from aiogram import F
from aiogram.filters import MagicData
from aiogram_dialog import Dialog

from .windows import action, statistics

DIALOG_NAME = "admin_dialog"

dialog = Dialog(
    action.window,
    statistics.window,
    name=DIALOG_NAME
)

dialog.callback_query.filter(
    MagicData(F["user_is_admin"].is_(True))
)
