from aiogram.fsm.state import State
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Const

from bot.general.dialogs.menu.states import MenuStates

MENU_TEXT = "Главное меню"
MENU_BTN_ID = "menu_btn"
MENU_BUTTON = Start(
    Const(MENU_TEXT),
    id=MENU_BTN_ID,
    state=MenuStates.menu
)

BACK_TEXT = "Назад"
BACK_BTN_ID = "back_btn"


def back_button(
        state: State,
        prev_dialog: bool = False
):
    if prev_dialog:
        return Cancel(
            Const(BACK_TEXT),
            id=BACK_BTN_ID,
        )
    return SwitchTo(
        Const(BACK_TEXT),
        id=BACK_BTN_ID,
        state=state
    )
