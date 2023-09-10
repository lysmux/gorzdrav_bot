from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot import bot_asnwers

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(text=bot_asnwers.ABOUT_BOT)


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(text=bot_asnwers.HELP)


@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=bot_asnwers.CANCELED)


@router.message()
async def unknown_command_handler(message: types.Message):
    await message.answer(text=bot_asnwers.UNKNOWN_COMMAND.format(command=message.text))
