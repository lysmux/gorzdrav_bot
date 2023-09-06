from aiogram.utils.keyboard import ReplyKeyboardBuilder

from models.gorzdrav import BaseItem


def generate_keyboard(items: list[BaseItem]):
    keyboard = ReplyKeyboardBuilder()

    for item in items:
        keyboard.button(text=item.name)

    keyboard.adjust(2, repeat=True)

    return keyboard.as_markup()
