from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Start
from aiogram_dialog.widgets.text import Jinja, Const

from src.bot.logic.dialogs.admin.states import AdminStates
from src.bot.logic.dialogs.general.states import GeneralStates
from src.bot.logic.dialogs.make_appointment.states import AppointmentStates
from src.bot.logic.dialogs.manage_tracking.states import TrackingStates
from src.bot.multimedia import keyboard_texts

MAKE_APPOINTMENT_BTN_ID = "make_appointment_btn"
MANAGE_TRACKING_BTN_ID = "manage_tracking_btn"
ADMIN_PANEL_BTN_ID = "admin_panel_btn"

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
        Start(
            Const(keyboard_texts.general.ADMIN_PANEL),
            when=F["middleware_data"]["user_is_admin"].is_(True),
            id=ADMIN_PANEL_BTN_ID,
            state=AdminStates.action
        ),
        width=2
    ),
    state=GeneralStates.menu
)
