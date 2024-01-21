import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.common import sync_scroll
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import (
    List, Format,
    Jinja, Const
)

from src.bot.logic.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_back_button
from .getter import data_getter
from .handlers import select_clinic

KB_HEIGHT = 3
KB_WIDTH = 2

LIST_ID = "clinics_list"
SCROLL_ID = "clinics_scroll"
SELECT_ID = "clinics_select"

window = Window(
    Jinja("make_appointment/clinic/header.html"),
    Const(" "),
    List(
        Jinja("make_appointment/clinic/item.html"),
        sep="\n" * 2,
        items="clinics",
        id=LIST_ID,
        page_size=KB_WIDTH * KB_HEIGHT
    ),
    ScrollingGroup(
        Select(
            Format("{item[1].short_name}"),
            items="clinics",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=select_clinic
        ),
        id=SCROLL_ID,
        on_page_changed=sync_scroll(LIST_ID),
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    get_back_button(AppointmentStates.district),
    getter=data_getter,
    state=AppointmentStates.clinic
)
