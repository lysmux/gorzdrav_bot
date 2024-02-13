from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo
from aiogram_dialog.widgets.text import Jinja, Const

from src.bot.logic.dialogs.manage_tracking.states import TrackingStates
from src.bot.multimedia import keyboard_texts
from src.bot.utils.buttons import get_menu_button

SHOW_TRACKING_BTN_ID = "show_tracking_btn"

window = Window(
    Jinja("tracking/deleted_header.html"),
    Group(
        SwitchTo(
            text=Const(keyboard_texts.general.SHOW_TRACKING),
            id=SHOW_TRACKING_BTN_ID,
            state=TrackingStates.list
        ),
        get_menu_button(),
        width=2
    ),
    state=TrackingStates.deleted,
)
