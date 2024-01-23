from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Button
from aiogram_dialog.widgets.text import Jinja, Const

from src.bot.logic.manage_tracking.states import TrackingStates
from src.bot.multimedia import keyboard_texts
from src.bot.utils.buttons import get_back_button
from .handlers import delete_tracking

STATUS_BTN_ID = "action_status_btn"
DELETE_BTN_ID = "action_delete_btn"

window = Window(
    Jinja("tracking/action_header.html"),
    Group(
        SwitchTo(
            Const(keyboard_texts.tracking.STATUS),
            id=STATUS_BTN_ID,
            state=TrackingStates.status
        ),
        Button(
            Const(keyboard_texts.tracking.DELETE),
            id=DELETE_BTN_ID,
            on_click=delete_tracking
        ),
        width=2
    ),
    get_back_button(TrackingStates.list),
    state=TrackingStates.action
)
