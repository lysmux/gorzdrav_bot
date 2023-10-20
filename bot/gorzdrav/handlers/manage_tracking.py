from aiogram import Router, types
from aiogram.filters import Command

from bot.gorzdrav.keyboards import paginator_items
from bot.gorzdrav.keyboards.callbacks import TrackingCallback
from bot.utils.inline_paginator import Paginator
from bot.utils.template_engine import render_template
from database.database import Repository

router = Router()


@router.message(Command("tracking"))
async def tracking_list_handler(
        message: types.Message,
        repository: Repository
):
    user_tracking = await repository.get_user_tracking(tg_user_id=message.from_user.id)
    items = paginator_items.tracking_items_factory(user_tracking)

    if items:
        paginator = Paginator(
            router=router,
            name="tracking",
            header_text=render_template("gorzdrav/tracking/tracking_header.html"),
            items=items
        )

        await paginator.send_paginator(message)
    else:
        await message.answer(text=render_template("gorzdrav/tracking/no_tracking.html"))


@router.callback_query(
    TrackingCallback.filter()
)
async def remove_tracking_handler(
        call: types.CallbackQuery,
        callback_data: TrackingCallback,
        repository: Repository
):
    await repository.delete_tracking(tracking_id=callback_data.id)
    await call.message.edit_text(
        text=render_template("gorzdrav/tracking/tracking_deleted.html", tracking_id=callback_data.id)
    )
