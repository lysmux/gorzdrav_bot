from typing import Generator

from aiogram import Router, F, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel

from bot.utils.template_engine import render_template


class PaginatorItem(BaseModel):
    text: str = ""
    button: InlineKeyboardButton


class PaginatorCallback(CallbackData, prefix="paginator"):
    name: str
    page: int


class Paginator:
    def __init__(
            self,
            router: Router,
            name: str,
            header_text: str,
            items: list[PaginatorItem],
            static_markup: InlineKeyboardMarkup | None = None,
            items_per_page: int = 6,
            keyboard_width: int = 2,
            page_separator: str = "/",
    ):
        if static_markup:
            self.static_builder = InlineKeyboardBuilder.from_markup(static_markup)
            self.static_builder.adjust(keyboard_width)
        else:
            self.static_builder = InlineKeyboardBuilder()

        self.current_page = 1

        self.router = router
        self.name = name
        self.keyboard_width = keyboard_width
        self.page_separator = page_separator

        self.header_text = header_text
        self.items = list(self.batch(items, items_per_page))

        self.register_paginator_handler()

    @staticmethod
    def batch(iterable, size) -> Generator:
        iter_len = len(iterable)
        for idx in range(0, iter_len, size):
            yield iterable[idx:min(idx + size, iter_len)]

    def get_paginator(self) -> list[InlineKeyboardButton]:
        buttons = [
            InlineKeyboardButton(
                text=f"{self.current_page}{self.page_separator}{len(self.items)}",
                callback_data=PaginatorCallback(name=self.name, page=0).pack()
            )]

        if self.current_page > 1:
            buttons = [
                          InlineKeyboardButton(
                              text="⏮️️",
                              callback_data=PaginatorCallback(name=self.name, page=1).pack()
                          ),
                          InlineKeyboardButton(
                              text="⬅️",
                              callback_data=PaginatorCallback(name=self.name, page=self.current_page - 1).pack()
                          )
                      ] + buttons

        if len(self.items) > self.current_page:
            buttons = buttons + [
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=PaginatorCallback(name=self.name, page=self.current_page + 1).pack()
                ),
                InlineKeyboardButton(
                    text="⏭️",
                    callback_data=PaginatorCallback(name=self.name, page=len(self.items)).pack()
                )
            ]
        return buttons

    def get_markup(self) -> InlineKeyboardMarkup:
        paginator = self.get_paginator()
        items = self.items[self.current_page - 1]

        builder = InlineKeyboardBuilder()
        for item in items:
            builder.add(item.button)

        builder.adjust(self.keyboard_width, repeat=True)
        builder.row(*paginator)
        builder.attach(self.static_builder)

        return builder.as_markup(resize=True)

    def get_text(self) -> str:
        items = self.items[self.current_page - 1]

        return render_template("paginator/paginator.html",
                               header=self.header_text,
                               items=items)

    def register_paginator_handler(self):
        @self.router.callback_query(PaginatorCallback.filter(F.name == self.name))
        async def handler(call: CallbackQuery, callback_data: PaginatorCallback):
            await call.answer()

            if callback_data.page:
                self.current_page = callback_data.page
                await self.update_paginator(call)

    async def send_paginator_by_bot(self, bot: Bot, chat_id: int):
        await bot.send_message(
            chat_id=chat_id,
            text=self.get_text(),
            reply_markup=self.get_markup()
        )

    async def send_paginator(self, message: Message):
        await self.send_paginator_by_bot(bot=message.bot, chat_id=message.chat.id)

    async def update_paginator_by_bot(
            self,
            bot: Bot,
            chat_id: int,
            message_id: int
    ):
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=self.get_text(),
            reply_markup=self.get_markup()
        )

    async def update_paginator(self, call: CallbackQuery):
        await self.update_paginator_by_bot(
            bot=call.bot,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
