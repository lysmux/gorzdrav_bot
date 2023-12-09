from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Start
from aiogram_dialog.widgets.text import Jinja, Const

from bot import keyboard_texts
from bot.logic.general.states import MenuStates
from bot.logic.make_appointment.states import AppointmentStates
from bot.logic.manage_tracking.states import TrackingStates

MAKE_APPOINTMENT_BTN_ID = "make_appointment_btn"
MANAGE_TRACKING_BTN_ID = "manage_tracking_btn"

window = Window(
    Jinja("general/menu.html"),
    Group(
        Start(
            Const(keyboard_texts.general.MAKE_APPOINTMENT),
            id=MAKE_APPOINTMENT_BTN_ID,
            state=AppointmentStates.district
        ),
        Start(
            Const(keyboard_texts.general.SHOW_TRACKING),
            id=MANAGE_TRACKING_BTN_ID,
            state=TrackingStates.list
        ),
        width=2
    ),
    state=MenuStates.menu
)
