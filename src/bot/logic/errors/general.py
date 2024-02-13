from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager

from src.database import Repository
from src.database.models import UserModel

ROUTER_NAME = "general_errors"

router = Router(name=ROUTER_NAME)


@router.error(ExceptionTypeFilter(TelegramForbiddenError))
async def forbidden_error_handler(
        event: ErrorEvent,
        user: UserModel,
        repository: Repository,
        dialog_manager: DialogManager
) -> None:
    """
    Handle error when user blocked bot. Delete user from DB and redis cache
    """

    await repository.user.delete(
        clause=UserModel.id == user.id
    )
    await dialog_manager.reset_stack()
