from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("make_appointment"))
async def make_appointment_handler(message: types.Message):
    await message.answer(text="Выбери свой район. В дальнейшем его можно будет изменить в настройках")
