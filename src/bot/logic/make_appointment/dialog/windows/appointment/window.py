import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup, ListGroup,
    Url, Group,
    SwitchTo
)
from aiogram_dialog.widgets.text import (
    Format, Jinja,
    Case, Const
)

from src.bot.logic.make_appointment.states import AppointmentStates
from src.bot.multimedia import keyboard_texts
from src.bot.utils.buttons import get_menu_button, get_back_button
from .getter import data_getter

KB_HEIGHT = 4
KB_WIDTH = 2

SCROLL_ID = "appointments_scroll"
LIST_ID = "appointments_list"
ADD_TRACKING_BTN_ID = "add_tracking_btn"

window = Window(
    Case(
        {
            False: Jinja("make_appointment/appointment/header.html"),
            True: Jinja("make_appointment/appointment/no_appointments.html"),
        },
        selector=F["appointments"].len() == 0
    ),
    ScrollingGroup(
        ListGroup(
            Url(
                text=Format("{item[1].time_str}"),
                url=Format("{data[appointment_url]}")
            ),
            items="appointments",
            item_id_getter=operator.itemgetter(0),
            id=LIST_ID
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    SwitchTo(
        Const(keyboard_texts.make_appointment.ADD_TRACKING),
        id=ADD_TRACKING_BTN_ID,
        state=AppointmentStates.tracking_add
    ),
    Group(
        get_back_button(AppointmentStates.doctor),
        get_menu_button(),
        width=2
    ),
    getter=data_getter,
    state=AppointmentStates.appointment
)
