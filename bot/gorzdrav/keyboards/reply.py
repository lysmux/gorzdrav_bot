from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pydantic import BaseModel


def generate_keyboard(items: list[BaseModel]):
    keyboard = ReplyKeyboardBuilder()

    for item in items:
        keyboard.button(text=item.name)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
