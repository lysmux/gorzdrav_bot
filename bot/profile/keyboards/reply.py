from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot import bot_asnwers
from database.models.profile import Profile


def generate_profiles_keyboard(profiles: List[Profile]):
    builder = ReplyKeyboardBuilder()

    for profile in profiles:
        builder.button(text=bot_asnwers.PROFILE_KEYBOARD.format(
            last_name=profile.last_name,
            first_name=profile.first_name,
            middle_name=profile.middle_name,
            birthdate=profile.birthdate.strftime("%d.%m.%Y"),
        ))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
