import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.common import sync_scroll
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import (
    Format, Const,
    List, Jinja
)

from src.bot.logic.dialogs.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_back_button
from .getter import data_getter
from .handlers import select_doctor

KB_HEIGHT = 3
KB_WIDTH = 2

LIST_ID = "doctors_list"
SCROLL_ID = "doctors_scroll"
SELECT_ID = "doctors_select"

window = Window(
    Jinja("make_appointment/doctor/header.html"),
    Const(" "),
    List(
        Jinja("make_appointment/doctor/item.html"),
        sep="\n" * 2,
        items="doctors",
        id=LIST_ID,
        page_size=KB_WIDTH * KB_HEIGHT
    ),
    ScrollingGroup(
        Select(
            Format("{item[1].short_name}"),
            items="doctors",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=select_doctor
        ),
        id=SCROLL_ID,
        on_page_changed=sync_scroll(LIST_ID),
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    get_back_button(AppointmentStates.speciality),
    getter=data_getter,
    state=AppointmentStates.doctor
)
