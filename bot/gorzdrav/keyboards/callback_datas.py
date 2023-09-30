from enum import Enum

from aiogram.filters.callback_data import CallbackData


class TimeRange(Enum):
    all_day = 0
    morning = 1
    afternoon = 2
    evening = 3


class TimeRangeCallback(CallbackData, prefix="time_range"):
    time_range: TimeRange
