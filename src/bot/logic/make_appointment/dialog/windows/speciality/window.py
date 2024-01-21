import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Jinja

from src.bot.logic.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_back_button
from .getter import data_getter
from .handlers import select_speciality

KB_HEIGHT = 4
KB_WIDTH = 1

SCROLL_ID = "specialities_scroll"
SELECT_ID = "specialities_select"

window = Window(
    Jinja("make_appointment/speciality/header.html"),
    ScrollingGroup(
        Select(
            Format("{item[1].name}"),
            items="specialities",
            item_id_getter=operator.itemgetter(0),
            id=SELECT_ID,
            type_factory=int,
            on_click=select_speciality
        ),
        id=SCROLL_ID,
        height=KB_HEIGHT,
        width=KB_WIDTH
    ),
    get_back_button(AppointmentStates.clinic),
    getter=data_getter,
    state=AppointmentStates.speciality
)
