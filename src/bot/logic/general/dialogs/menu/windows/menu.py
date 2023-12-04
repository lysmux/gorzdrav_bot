from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Start
from aiogram_dialog.widgets.text import Const, Jinja

from src.bot.logic.general.dialogs.menu import button_texts
from src.bot.logic.general.dialogs.menu.states import MenuStates
from src.bot.logic.gorzdrav.dialogs.appointment.states import AppointmentStates
from src.bot.logic.gorzdrav.dialogs.manage_tracking.states import TrackingStates

MAKE_APPOINTMENT_BTN_ID = "make_appointment_btn"
MANAGE_TRACKING_BTN_ID = "manage_tracking_btn"

window = Window(
    Jinja("general/menu.html"),
    Group(
        Start(
            Const(button_texts.MAKE_APPOINTMENT),
            id=MAKE_APPOINTMENT_BTN_ID,
            state=AppointmentStates.district
        ),
        Start(
            Const(button_texts.MANAGE_TRACKING),
            id=MANAGE_TRACKING_BTN_ID,
            state=TrackingStates.list
        ),
        width=2
    ),
    state=MenuStates.menu
)
