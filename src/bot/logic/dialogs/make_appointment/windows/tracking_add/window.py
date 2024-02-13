import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Jinja, Format, Const

from src.bot.logic.dialogs.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_back_button
from .getter import data_getter, TimeRangeEnum
from .handlers import (
    process_raw_time_range,
    select_time_range,
    select_raw_time_range,
    raw_time_range_error
)

SELECT_ID = "time_range_select"
TEXT_INPUT_ID = "time_range_input"

window = Window(
    Jinja("errors/range_error.html",
          when=F["dialog_data"]["has_error"].is_(True)),
    Const(" "),
    Jinja("tracking/enter_time_range.html"),

    Group(
        Select(
            Format("{item[0]}"),
            id=SELECT_ID,
            item_id_getter=operator.itemgetter(1),
            items="ranges",
            on_click=select_time_range,
            type_factory=TimeRangeEnum
        ),
        width=2
    ),

    get_back_button(AppointmentStates.appointment),

    TextInput(
        id=TEXT_INPUT_ID,
        type_factory=process_raw_time_range,
        on_success=select_raw_time_range,
        on_error=raw_time_range_error
    ),

    getter=data_getter,
    state=AppointmentStates.tracking_add
)
