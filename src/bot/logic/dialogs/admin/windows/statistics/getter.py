from src.database import Repository


async def data_getter(
        repository: Repository,
        **kwargs
) -> dict[str, int]:
    users_count = await repository.user.count()
    tracking_count = await repository.tracking.count()

    return {
        "users_count": users_count,
        "tracking_count": tracking_count,
    }
