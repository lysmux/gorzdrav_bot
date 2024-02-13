from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Jinja

from src.bot.logic.dialogs.admin.states import AdminStates
from src.bot.utils.buttons import get_back_button
from .getter import data_getter

window = Window(
    Jinja("admin/statistics.html"),
    get_back_button(AdminStates.action),
    getter=data_getter,
    state=AdminStates.statistics
)
