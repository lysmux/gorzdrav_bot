from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Jinja

from src.bot.logic.admin.states import AdminStates
from src.bot.utils.buttons import get_back_button
from src.database import Repository


async def data_getter(
        repository: Repository,
        **kwargs
) -> dict:
    users_count = await repository.user.count()
    tracking_count = await repository.tracking.count()

    return {
        "users_count": users_count,
        "tracking_count": tracking_count,
    }


window = Window(
    Jinja("admin/statistics.html"),
    get_back_button(AdminStates.action),
    getter=data_getter,
    state=AdminStates.statistics
)
