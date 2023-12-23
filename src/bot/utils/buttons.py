from aiogram.fsm.state import State
from aiogram_dialog.widgets.kbd import Start, Back, SwitchTo
from aiogram_dialog.widgets.text import Const

from src.bot import keyboard_texts
from src.bot.logic.general.states import MenuStates

MENU_BTN_ID = "menu_btn"
BACK_BTN_ID = "back_btn"


def get_menu_button() -> Start:
    return Start(
        Const(keyboard_texts.general.MENU),
        id=MENU_BTN_ID,
        state=MenuStates.menu
    )


def get_back_button(state: State):
    return SwitchTo(
        Const(keyboard_texts.general.BACK),
        id=BACK_BTN_ID,
        state=state
    )
