from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.gorzdrav.keyboards import buttons_texts
from bot.gorzdrav.keyboards import callbacks


def tracking_keyboard_factory():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=buttons_texts.ADD_TO_TRACKER,
                                 callback_data=callbacks.AddTrackingCallback().pack())
        ]
    ])

    return keyboard


def time_range_keyboard_factory():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=buttons_texts.MORNING,
                                 callback_data=callbacks.TimeRangeCallback(
                                     time_range=callbacks.TimeRange.morning
                                 ).pack()),
            InlineKeyboardButton(text=buttons_texts.AFTERNOON,
                                 callback_data=callbacks.TimeRangeCallback(
                                     time_range=callbacks.TimeRange.afternoon
                                 ).pack()),
            InlineKeyboardButton(text=buttons_texts.EVENING,
                                 callback_data=callbacks.TimeRangeCallback(
                                     time_range=callbacks.TimeRange.evening
                                 ).pack()),
        ],
        [
            InlineKeyboardButton(text=buttons_texts.ALL_DAY,
                                 callback_data=callbacks.TimeRangeCallback(
                                     time_range=callbacks.TimeRange.all_day
                                 ).pack()),
        ]
    ])

    return keyboard
