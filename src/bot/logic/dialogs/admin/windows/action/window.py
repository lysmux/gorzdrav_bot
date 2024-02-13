from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja

from src.bot.logic.dialogs.admin.states import AdminStates
from src.bot.multimedia import keyboard_texts
from src.bot.utils.buttons import get_menu_button

STATISTICS_BTN_ID = "statistics_btn"

window = Window(
    Jinja("admin/action.html"),
    SwitchTo(
        text=Const(keyboard_texts.admin.STATISTICS),
        id=STATISTICS_BTN_ID,
        state=AdminStates.statistics
    ),
    get_menu_button(),
    state=AdminStates.action
)
