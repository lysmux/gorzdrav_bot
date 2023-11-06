from aiogram import Router

from bot.general.dialogs import menu

router = Router()

router.include_routers(menu.dialog)
