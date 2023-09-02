from idlelib.undo import CommandSequence

from aiogram import Router, types
from aiogram.filters import CommandStart, Command

import bot_asnwers

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(text=bot_asnwers.ABOUT_BOT)


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(text=bot_asnwers.HELP)
