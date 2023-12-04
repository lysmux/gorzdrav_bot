from aiogram_dialog import Dialog

from src.bot.logic.gorzdrav.dialogs.add_tracking.windows import add
from src.bot.logic.gorzdrav.dialogs.add_tracking.windows import added

dialog = Dialog(
    add.window,
    added.window
)
