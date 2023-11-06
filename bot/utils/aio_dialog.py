from typing import Callable, Awaitable

from aiogram_dialog import ChatEvent
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll


def sync_scroll(scroll_id: str) -> Callable[
    [ChatEvent, ManagedScroll, DialogManager],
    Awaitable[None],
]:
    async def on_page_changed(
            event: ChatEvent,
            widget: ManagedScroll,
            dialog_manager: DialogManager,
    ) -> None:
        page = await widget.get_page()
        other_scroll: ManagedScroll = dialog_manager.find(scroll_id)
        await other_scroll.set_page(page=page)

    return on_page_changed
