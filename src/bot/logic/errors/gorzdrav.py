from typing import cast

from aiogram import Router, Bot
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, User

from src.bot.utils.template_engine import render_template
from src.gorzdrav_api.exceptions import GorZdravError

router = Router()


@router.error(ExceptionTypeFilter(GorZdravError))
async def server_error_handler(
        event: ErrorEvent,
        event_from_user: User,
        bot: Bot
) -> None:
    exception = cast(GorZdravError, event.exception)
    await bot.send_message(
        chat_id=event_from_user.id,
        text=render_template("errors/api_error.html", error_msg=exception.message)
    )
