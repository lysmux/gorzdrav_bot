from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.utils.template_engine import render_template

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(text=render_template("common/about.html"))


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(text=render_template("common/help.html"))


@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=render_template("common/action_canceled.html"))


@router.message()
async def unknown_command_handler(message: types.Message):
    await message.answer(text=render_template("common/unknown_command.html", command=message.text))
