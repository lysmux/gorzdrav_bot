from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    ScrollingGroup, ListGroup,
    Url, Group
)
from aiogram_dialog.widgets.text import Jinja, Format, Case

from src.bot.logic.dialogs.manage_tracking.states import TrackingStates
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
            None: Jinja("tracking/status_header.html"),
            "not_exists": Jinja("tracking/not_exists.html"),
            "no_appointments": Jinja("make_appointment/appointment/no_appointments.html")
        },
        selector=F["error"]
    ),

    # Appointments keyboard
    ScrollingGroup(
        ListGroup(
            Url(
                text=Format("{item.time_str}"),
                url=Format("{data[appointment_url]}")
            ),
            items="appointments",
            item_id_getter=lambda data: "url",
            id=LIST_ID
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH,
        when=F.not_contains("error") | F["error"].is_(None)
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
