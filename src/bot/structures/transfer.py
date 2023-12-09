from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncEngine

from database import Repository
from gorzdrav_api import GorZdravAPI


class TransferStruct(TypedDict, total=False):
    engine: AsyncEngine
    repository: Repository
    gorzdrav_api: GorZdravAPI
