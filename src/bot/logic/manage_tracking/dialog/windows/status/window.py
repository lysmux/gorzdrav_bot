import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup, ListGroup,
    Url, Group
)
from aiogram_dialog.widgets.text import Jinja, Format, Case

from src.bot.logic.manage_tracking.states import TrackingStates
from src.bot.utils.buttons import get_back_button, get_menu_button
from .getter import data_getter

KB_HEIGHT = 4
KB_WIDTH = 2

SCROLL_ID = "status_scroll"
LIST_ID = "status_list"

window = Window(
    # Text
    Case(
        {
            False: Jinja("tracking/status_header.html"),
            True: Jinja("make_appointment/appointment/no_appointments.html"),
        },
        selector=F["filtered_appointments"].len() == 0
    ),

    # Appointments keyboard
    ScrollingGroup(
        ListGroup(
            Url(
                text=Format("{item[1].time_str}"),
                url=Format("{data[appointment_url]}")
            ),
            items="filtered_appointments",
            item_id_getter=operator.itemgetter(0),
            id=LIST_ID
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),

    # Navigation
    Group(
        get_back_button(TrackingStates.list),
        get_menu_button(),
        width=2
    ),
    getter=data_getter,
    state=TrackingStates.status
)
