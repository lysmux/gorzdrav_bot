from typing import Generator

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.template_engine import render_template


def batch(iterable, size) -> Generator:
    iter_len = len(iterable)
    for idx in range(0, iter_len, size):
        yield iterable[idx:min(idx + size, iter_len)]


class PaginatorCallback(CallbackData, prefix="paginator"):
    name: str
    page: int


class Paginator:
    def __init__(
            self,
            router: Router,
            name: str,
            header_text: str,
            buttons: list[InlineKeyboardButton],
            texts: list[str] | None = None,
            items_per_page: int = 6,
            keyboard_width: int = 2,
            page_separator: str = "/",
    ):
        if texts and len(texts) != len(buttons):
            raise ValueError("Length of list[texts] should be equal to length of list[buttons]")

        self.current_page = 1

        self.router = router
        self.name = name
        self.keyboard_width = keyboard_width
        self.page_separator = page_separator

        self.header_text = header_text
        self.buttons = list(batch(buttons, items_per_page))
        self.texts = list(batch(texts, items_per_page)) if texts else None

        self.register_paginator_handler()

    def get_paginator(self) -> list[InlineKeyboardButton]:
        buttons = [
            InlineKeyboardButton(
                text=f"{self.current_page}{self.page_separator}{len(self.buttons)}",
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

        if len(self.buttons) > self.current_page:
            buttons = buttons + [
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=PaginatorCallback(name=self.name, page=self.current_page + 1).pack()
                ),
                InlineKeyboardButton(
                    text="⏭️",
                    callback_data=PaginatorCallback(name=self.name, page=len(self.buttons)).pack()
                )
            ]
        return buttons

    def get_markup(self) -> InlineKeyboardMarkup:
        paginator = self.get_paginator()
        buttons = self.buttons[self.current_page - 1]

        builder = InlineKeyboardBuilder()
        builder.add(*buttons)
        builder.adjust(self.keyboard_width, repeat=True)
        builder.row(*paginator)

        return builder.as_markup(resize=True)

    def get_text(self) -> str:
        page_texts = self.texts[self.current_page - 1]

        return render_template("paginator.html",
                               header=self.header_text,
                               texts=page_texts)

    def register_paginator_handler(self):
        @self.router.callback_query(PaginatorCallback.filter(F.name == self.name))
        async def handler(call: CallbackQuery, callback_data: PaginatorCallback):
            await call.answer()

            if callback_data.page:
                self.current_page = callback_data.page
                await call.message.edit_text(text=self.get_text(), reply_markup=self.get_markup())

    async def send_paginator(self, message: Message):
        await message.answer(
            text=self.get_text(),
            reply_markup=self.get_markup()
        )
