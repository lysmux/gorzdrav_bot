import re

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot.gorzdrav.keyboards import inline
from bot.gorzdrav.keyboards.callbacks import AddTrackingCallback, TimeRangeCallback, TimeRange
from bot.gorzdrav.states import AppointmentStates, TrackingStates
from bot.utils.template_engine import render_template
from database.database import Repository

router = Router()
router.callback_query.middleware(CallbackAnswerMiddleware())


@router.callback_query(
    AppointmentStates.appointment,
    AddTrackingCallback.filter()
)
async def add_tracking_handler(
        call: types.CallbackQuery,
        state: FSMContext
):
    markup = inline.time_range_mp()
    await call.message.edit_text(text=render_template("gorzdrav/tracking/enter_time_range.html"),
                                 reply_markup=markup)
    await state.set_state(TrackingStates.time_range)


@router.message(TrackingStates.time_range)
async def raw_time_range_handler(
        message: types.Message,
        state: FSMContext,
        repository: Repository
):
    selected_hours = set()
    raw_time_ranges = re.findall(r"(\d*)-(\d*)", message.text)
    for hour_from, hour_to in raw_time_ranges:
        hour_from = int(hour_from)
        hour_to = int(hour_to)

        if hour_from not in range(24):
            error_text = render_template("gorzdrav/tracking/time_range/range_error.html",
                                         hour_from=hour_from,
                                         hour_to=hour_to,
                                         value=hour_from)
            await message.answer(text=error_text)
            return
        if hour_to not in range(24):
            error_text = render_template("gorzdrav/tracking/time_range/range_error.html",
                                         hour_from=hour_from,
                                         hour_to=hour_to,
                                         value=hour_to)
            await message.answer(text=error_text)
            return
        if hour_from >= hour_to:
            error_text = render_template("gorzdrav/tracking/time_range/time_error.html",
                                         hour_from=hour_from,
                                         hour_to=hour_to)
            await message.answer(text=error_text)
            return

        time_range = set(range(hour_from, hour_to))
        selected_hours.update(time_range)

    state_data = await state.get_data()
    district = state_data.get("selected_district")
    clinic = state_data.get("selected_clinic")
    speciality = state_data.get("selected_speciality")
    doctor = state_data.get("selected_doctor")

    await repository.add_tracking(
        tg_user_id=message.from_user.id,
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
        hours=list(selected_hours)
    )
    await state.clear()
    await message.answer(text=render_template("gorzdrav/tracking/tracking_added.html"))
    await message.bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )


@router.callback_query(
    TrackingStates.time_range,
    TimeRangeCallback.filter()
)
async def time_range_handler(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: TimeRangeCallback,
        repository: Repository
):
    match callback_data.time_range:
        case TimeRange.morning:
            selected_hours = list(range(13))
        case TimeRange.afternoon:
            selected_hours = list(range(13, 18))
        case TimeRange.evening:
            selected_hours = list(range(18, 24))
        case TimeRange.all_day:
            selected_hours = list(range(24))
        case _:
            selected_hours = []

    state_data = await state.get_data()
    district = state_data.get("selected_district")
    clinic = state_data.get("selected_clinic")
    speciality = state_data.get("selected_speciality")
    doctor = state_data.get("selected_doctor")

    await repository.add_tracking(
        tg_user_id=call.from_user.id,
        district=district,
        clinic=clinic,
        speciality=speciality,
        doctor=doctor,
        hours=selected_hours
    )
    await state.clear()
    await call.message.edit_text(text=render_template("gorzdrav/tracking/tracking_added.html"))
