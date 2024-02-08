from typing import TypedDict

from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import User
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database import Repository
from src.database.models import UserModel
from src.gorzdrav_api import GorZdravAPI
from src.services.appointments_checker import StorageProxy


class TransferStruct(TypedDict, total=False):
    bot: Bot
    event_from_user: User
    fsm_storage: BaseStorage

    session_maker: async_sessionmaker
    repository: Repository
    storage_proxy: StorageProxy

    gorzdrav_api: GorZdravAPI

    user: UserModel
    user_is_admin: bool
