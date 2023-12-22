import operator
import re
from enum import auto, StrEnum

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Jinja, Format, Const

from src.bot import keyboard_texts
from src.bot.logic.make_appointment.states import AppointmentStates
from src.bot.utils.buttons import get_back_button
from src.database.models import UserModel
from src.database.repositories import Repository
from src.gorzdrav_api.schemas import (
    District, Clinic, Speciality, Doctor
)

WINDOW_NAME = "add_tracking"
SELECT_ID = f"{WINDOW_NAME}_time_range_select"
TEXT_INPUT_ID = f"{WINDOW_NAME}_time_range_input"


class TimeRangeEnum(StrEnum):
    ALL_DAY = auto()
    MORNING = auto()
    AFTERNOON = auto()
    EVENING = auto()


async def data_getter(**kwargs) -> dict:
    return {
        "ranges": (
            (keyboard_texts.tracking.MORNING, TimeRangeEnum.MORNING),
            (keyboard_texts.tracking.AFTERNOON, TimeRangeEnum.AFTERNOON),
            (keyboard_texts.tracking.EVENING, TimeRangeEnum.EVENING),
            (keyboard_texts.tracking.ALL_DAY, TimeRangeEnum.ALL_DAY),
        )
    }


async def save_tracking(
        manager: DialogManager,
        time_ranges: list[list[int]]
) -> None:
    repository: Repository = manager.middleware_data["repository"]
    user: UserModel = manager.middleware_data["user"]

    district: District = manager.dialog_data["district"]
    clinic: Clinic = manager.dialog_data["clinic"]
    speciality: Speciality = manager.dialog_data["speciality"]
    doctor: Doctor = manager.dialog_data["doctor"]

    await repository.tracking.new(
        user=user,
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
        time_ranges=time_ranges
    )

    await manager.switch_to(AppointmentStates.tracking_added)


async def select_time_range(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        time_range: TimeRangeEnum,
) -> None:
    match time_range:
        case TimeRangeEnum.MORNING:
            time_range = [0, 13]
        case TimeRangeEnum.AFTERNOON:
            time_range = [13, 18]
        case TimeRangeEnum.EVENING:
            time_range = [18, 24]
        case TimeRangeEnum.ALL_DAY:
            time_range = [0, 23]
        case _:
            time_range = []

    await save_tracking(
        manager=manager,
        time_ranges=[time_range]
    )


async def select_raw_time_range(
        message: Message,
        widget: ManagedTextInput,
        manager: DialogManager,
        time_ranges
) -> None:
    await save_tracking(
        manager=manager,
        time_ranges=time_ranges
    )


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


async def raw_time_range_error(
        message: Message,
        widget: ManagedTextInput,
        manager: DialogManager,
        error: ValueError
) -> None:
    manager.dialog_data.update({"has_error": True})


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

    get_back_button(),

    TextInput(
        id=TEXT_INPUT_ID,
        type_factory=process_raw_time_range,
        on_success=select_raw_time_range,
        on_error=raw_time_range_error
    ),

    getter=data_getter,
    state=AppointmentStates.tracking_add
)
