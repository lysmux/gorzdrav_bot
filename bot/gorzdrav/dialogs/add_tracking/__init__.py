from aiogram_dialog import Dialog

from bot.gorzdrav.dialogs.add_tracking.windows import add, added

dialog = Dialog(
    add.window,
    added.window
)
