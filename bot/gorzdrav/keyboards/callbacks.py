from enum import IntEnum

from aiogram.filters.callback_data import CallbackData


class TimeRange(IntEnum):
    all_day = 0
    morning = 1
    afternoon = 2
    evening = 3


class TimeRangeCallback(CallbackData, prefix="time_range"):
    time_range: TimeRange


class AddTrackingCallback(CallbackData, prefix="add_tracking"):
    pass


class TrackingCallback(CallbackData, prefix="tracking"):
    id: int


class DistrictCallback(CallbackData, prefix="district"):
    id: str


class ClinicCallback(CallbackData, prefix="clinic"):
    id: str


class SpecialityCallback(CallbackData, prefix="spec"):
    id: str


class DoctorCallback(CallbackData, prefix="doctor"):
    id: str


class AppointmentCallback(CallbackData, prefix="appointment", sep="#"):
    id: str
