from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bot_asnwers


class DeleteProfileCallback(CallbackData, prefix="delete_profile"):
    pass


class ConfirmCallback(CallbackData, prefix="confirm"):
    action: str


action_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=bot_asnwers.DELETE_PROFILE, callback_data=DeleteProfileCallback().pack())
    ]
])

confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=bot_asnwers.CONFIRM, callback_data=ConfirmCallback(action="confirm").pack()),
        InlineKeyboardButton(text=bot_asnwers.CANCEL, callback_data=ConfirmCallback(action="cancel").pack())
    ]
])
