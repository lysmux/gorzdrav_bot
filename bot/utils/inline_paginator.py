from aiogram import types, Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PaginatorCallback(CallbackData, prefix="paginator"):
    keyboard_name: str
    page: int


class Paginator:
    def __init__(
            self,
            router: Router,
            keyboard: types.InlineKeyboardMarkup | InlineKeyboardBuilder,
            keyboard_name: str,
            size: int = 5,
            page_separator: str = "/",
    ):
        self.router = router
        self.keyboard_name = keyboard_name
        self.page_separator = page_separator

        self.current_page = 1

        if isinstance(keyboard, types.InlineKeyboardMarkup):
            self.kb_buttons = list(
                self.batch(
                    iterable=keyboard.inline_keyboard,
                    size=size
                )
            )
        elif isinstance(keyboard, InlineKeyboardBuilder):
            self.kb_buttons = list(
                self.batch(
                    iterable=keyboard.export(),
                    size=size
                )
            )

        self.register_paginator_handler()

    @staticmethod
    def batch(iterable, size):
        iter_len = len(iterable)
        for idx in range(0, iter_len, size):
            yield iterable[idx:min(idx + size, iter_len)]

    def get_markup(self) -> types.InlineKeyboardMarkup:
        list_current_buttons = self.kb_buttons[self.current_page - 1]
        paginator = self._get_paginator()
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[*list_current_buttons, paginator])

        return keyboard

    def _get_paginator(self) -> list[types.InlineKeyboardButton]:
        buttons = [
            types.InlineKeyboardButton(
                text=f"{self.current_page}{self.page_separator}{len(self.kb_buttons)}",
                callback_data=PaginatorCallback(keyboard_name=self.keyboard_name, page=0).pack()
            )]

        if self.current_page > 1:
            buttons = [
                types.InlineKeyboardButton(
                    text="⏮️️",
                    callback_data=PaginatorCallback(keyboard_name=self.keyboard_name, page=1).pack()
                ),
                types.InlineKeyboardButton(
                    text="⬅️",
                    callback_data=PaginatorCallback(keyboard_name=self.keyboard_name, page=self.current_page - 1).pack()
                ),
                *buttons
            ]

        if len(self.kb_buttons) > self.current_page:
            buttons = [
                *buttons,
                types.InlineKeyboardButton(
                    text="➡️",
                    callback_data=PaginatorCallback(keyboard_name=self.keyboard_name, page=self.current_page + 1).pack()
                ),
                types.InlineKeyboardButton(
                    text="⏭️",
                    callback_data=PaginatorCallback(keyboard_name=self.keyboard_name, page=len(self.kb_buttons)).pack()
                )
            ]
        return buttons

    def register_paginator_handler(self):
        @self.router.callback_query(PaginatorCallback.filter(F.keyboard_name == self.keyboard_name))
        async def _handler(call: types.CallbackQuery, callback_data: PaginatorCallback):
            await call.answer()

            if callback_data.page:
                self.current_page = callback_data.page
                await call.message.edit_reply_markup(reply_markup=self.get_markup())
