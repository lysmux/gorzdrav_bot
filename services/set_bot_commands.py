from aiogram import Bot
from aiogram.types import BotCommand

commands = {
    "start": "Об этом боте",
    "help": "Помощь",
    "make_appointment": "Записаться на приём"
}


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        BotCommand(command=command, description=description)
        for command, description in commands.items()
    ])
