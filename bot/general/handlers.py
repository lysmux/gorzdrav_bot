from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.general.dialogs.menu.states import MenuStates
from bot.utils.template_engine import render_template

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MenuStates.menu, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(text=render_template("general/help.html"))


@router.message()
async def unknown_command_handler(message: Message):
    await message.answer(text=render_template("general/unknown_command.html", command=message.text))
