from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncEngine

from src.database import Repository
from src.database.models import UserModel
from src.gorzdrav_api import GorZdravAPI


class TransferStruct(TypedDict, total=False):
    engine: AsyncEngine
    repository: Repository
    gorzdrav_api: GorZdravAPI
    user: UserModel
    user_is_admin: bool
