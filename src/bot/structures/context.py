from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncEngine

from src.database.repositories import Repository


class ContextData(TypedDict, total=False):
    engine: AsyncEngine
    repository: Repository
