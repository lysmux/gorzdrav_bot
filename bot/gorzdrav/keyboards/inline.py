from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.gorzdrav.keyboards import button_texts
from bot.gorzdrav.keyboards.callback_datas import TimeRangeCallback, TimeRange, SelectTrackingCallback
from bot.utils.template_engine import render_template
from database.models.tracking import Tracking


def monitor_keyboard_factory():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=button_texts.ADD_TO_TRACKER, callback_data="tracker")
        ]
    ])

    return keyboard


def time_range_keyboard_factory():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=button_texts.MORNING,
                                 callback_data=TimeRangeCallback(time_range=TimeRange.morning).pack()),
            InlineKeyboardButton(text=button_texts.AFTERNOON,
                                 callback_data=TimeRangeCallback(time_range=TimeRange.afternoon).pack()),
            InlineKeyboardButton(text=button_texts.EVENING,
                                 callback_data=TimeRangeCallback(time_range=TimeRange.evening).pack()),
        ],
        [
            InlineKeyboardButton(text=button_texts.ALL_DAY,
                                 callback_data=TimeRangeCallback(time_range=TimeRange.all_day).pack()),
        ]
    ])

    return keyboard


def tracking_paginator_items_factory(tracking: Iterable[Tracking]) -> tuple[list[str], list[InlineKeyboardButton]]:
    texts = []
    buttons = []

    for track in tracking:
        texts.append(
            render_template("info/tracking_item.html", track=track)
        )
        buttons.append(InlineKeyboardButton(
            text=str(track.id),
            callback_data=SelectTrackingCallback(id=track.id).pack()
        ))

    return texts, buttons
