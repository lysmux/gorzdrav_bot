from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group
from aiogram_dialog.widgets.text import Jinja

from src.bot.logic.dialogs.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_menu_button, get_back_button

window = Window(
    Jinja("tracking/tracking_added.html"),
    Group(
        get_back_button(AppointmentStates.tracking_add),
        get_menu_button(),
        width=2
    ),
    state=AppointmentStates.tracking_added,
)
