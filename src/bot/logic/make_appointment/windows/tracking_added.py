from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.text import Jinja

from bot.utils.buttons import get_menu_button, get_back_button
from ..states import AppointmentStates

window = Window(
    Jinja("tracking/tracking_added.html"),
    Group(
        get_back_button(),
        get_menu_button(),
        width=2
    ),
    state=AppointmentStates.tracking_added,
)
