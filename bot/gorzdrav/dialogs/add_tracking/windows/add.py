import operator
import re
from enum import auto, StrEnum

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Jinja, Format, Const

from bot.gorzdrav.dialogs.add_tracking import button_texts
from bot.gorzdrav.dialogs.add_tracking.states import AddTrackingStates
from bot.gorzdrav.dialogs.appointment.states import AppointmentStates
from bot.misc.buttons import back_button
from database.database import Repository
from gorzdrav_api.schemas import (
    District,
    Doctor,
    Speciality,
    Clinic
)

WINDOW_NAME = "add_tracking"
SELECT_ID = f"{WINDOW_NAME}_time_range_select"
TEXT_INPUT_ID = f"{WINDOW_NAME}_time_range_input"


class TimeRange(StrEnum):
    ALL_DAY = auto()
    MORNING = auto()
    AFTERNOON = auto()
    EVENING = auto()


async def time_range_getter(**kwargs) -> dict:
    return {
        "ranges": (
            (button_texts.MORNING, TimeRange.MORNING),
            (button_texts.AFTERNOON, TimeRange.AFTERNOON),
            (button_texts.EVENING, TimeRange.EVENING),
            (button_texts.ALL_DAY, TimeRange.ALL_DAY),
        )
    }


async def time_range_handler(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        time_range: TimeRange,
):
    repository: Repository = manager.middleware_data["repository"]

    district: District = manager.start_data["district"]
    clinic: Clinic = manager.start_data["clinic"]
    speciality: Speciality = manager.start_data["speciality"]
    doctor: Doctor = manager.start_data["doctor"]

    match time_range:
        case TimeRange.MORNING:
            time_range = [0, 13]
        case TimeRange.AFTERNOON:
            time_range = [13, 18]
        case TimeRange.EVENING:
            time_range = [18, 24]
        case TimeRange.ALL_DAY:
            time_range = [0, 23]
        case _:
            time_range = []

    await repository.add_tracking(
        tg_user_id=callback.from_user.id,
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
        time_ranges=[time_range]
    )

    await manager.switch_to(AddTrackingStates.added)


def process_raw_time_range(text: str) -> list[list[int]]:
    time_ranges = []
    raw_time_ranges = re.findall(r"(\d*)-(\d*)", text)

    if not raw_time_ranges:
        raise ValueError

    for hour_from, hour_to in raw_time_ranges:
        hour_from = int(hour_from)
        hour_to = int(hour_to)

        if hour_from not in range(24):
            raise ValueError
        if hour_to not in range(24):
            raise ValueError
        if hour_from >= hour_to:
            raise ValueError

        time_ranges.append([hour_from, hour_to])
    return time_ranges


async def raw_time_range_handler(
        message: Message,
        widget: ManagedTextInput,
        manager: DialogManager,
        time_ranges
):
    repository: Repository = manager.middleware_data["repository"]

    district: District = manager.start_data["district"]
    clinic: Clinic = manager.start_data["clinic"]
    speciality: Speciality = manager.start_data["speciality"]
    doctor: Doctor = manager.start_data["doctor"]

    await repository.add_tracking(
        tg_user_id=message.from_user.id,
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
        time_ranges=time_ranges
    )
    await manager.switch_to(AddTrackingStates.added)


async def raw_time_range_error_handler(
        message: Message,
        widget: ManagedTextInput,
        manager: DialogManager,
        error: ValueError
):
    manager.dialog_data.update({"has_error": True})


window = Window(
    Jinja("gorzdrav/errors/range_error.html",
          when=F["dialog_data"]["has_error"].is_(True)),
    Const(" "),
    Jinja("gorzdrav/tracking/time_range.html"),
    Group(
        Select(
            Format("{item[0]}"),
            id=SELECT_ID,
            item_id_getter=operator.itemgetter(1),
            items="ranges",
            on_click=time_range_handler,
            type_factory=TimeRange
        ),
        width=2
    ),
    TextInput(
        id=TEXT_INPUT_ID,
        type_factory=process_raw_time_range,
        on_success=raw_time_range_handler,
        on_error=raw_time_range_error_handler
    ),
    back_button(state=AppointmentStates.appointment, prev_dialog=True),
    state=AddTrackingStates.add,
    getter=time_range_getter
)
