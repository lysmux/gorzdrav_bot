from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from bot.utils.template_engine import render_template
from gorzdrav_api.exceptions import GorZdravError

router = Router()


@router.error(ExceptionTypeFilter(GorZdravError))
async def server_error_handler(event: ErrorEvent) -> bool:
    if event.update.message:
        chat_id = event.update.message.from_user.id
    else:
        chat_id = event.update.callback_query.from_user.id

    await event.update.bot.send_message(
        chat_id=chat_id,
        text=render_template("errors/api_error.html")
    )

    return True
