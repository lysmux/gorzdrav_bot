from aiogram.fsm.state import State
from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const

from src.bot.logic.general.states import GeneralStates
from src.bot.multimedia import keyboard_texts

MENU_BTN_ID = "menu_btn"
BACK_BTN_ID = "back_btn"


def get_menu_button() -> Start:
    return Start(
        Const(keyboard_texts.general.MENU),
        id=MENU_BTN_ID,
        state=GeneralStates.menu,
        mode=StartMode.RESET_STACK
    )


def get_back_button(state: State):
    return SwitchTo(
        Const(keyboard_texts.general.BACK),
        id=BACK_BTN_ID,
        state=state
    )
