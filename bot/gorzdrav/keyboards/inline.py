from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot_asnwers


def monitor_keyboard_factory():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=bot_asnwers.ADD_TO_TRACKER, callback_data="tracker")
        ]
    ])

    return keyboard
