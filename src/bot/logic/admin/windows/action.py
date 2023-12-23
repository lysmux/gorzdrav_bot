from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja

from src.bot.logic.admin.states import AdminStates

WINDOW_NAME = "admin"
STATISTICS_BTN_ID = f"{WINDOW_NAME}_statistics_btn"

window = Window(
    Jinja("admin/action.html"),
    SwitchTo(
        text=Const("Статистика"),
        id=STATISTICS_BTN_ID,
        state=AdminStates.statistics
    ),
    state=AdminStates.action
)
