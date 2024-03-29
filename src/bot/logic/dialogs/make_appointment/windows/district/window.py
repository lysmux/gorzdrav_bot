import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Jinja

from src.bot.logic.dialogs.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_menu_button
from .getter import data_getter
from .handlers import select_district

KB_HEIGHT = 4
KB_WIDTH = 2

SCROLL_ID = "district_scroll"
SELECT_ID = "district_select"

window = Window(
    Jinja("make_appointment/district/header.html"),
    ScrollingGroup(
        Select(
            text=Format("{item[1].name}"),
            id=SELECT_ID,
            items="districts",
            item_id_getter=operator.itemgetter(0),
            type_factory=int,
            on_click=select_district
        ),
        id=SCROLL_ID,
        width=KB_WIDTH,
        height=KB_HEIGHT,
    ),
    get_menu_button(),
    getter=data_getter,
    state=AppointmentStates.district,
)
