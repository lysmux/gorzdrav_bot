from typing import Any

from src.database.models import UserModel


async def data_getter(
        user: UserModel,
        **kwargs
) -> dict[str, Any]:
    """
        Get user tracking from database
    """

    return {
        "user_tracking": user.tracking
    }
