import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.base import BaseStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.bot.multimedia import keyboard_texts
from src.bot.utils.template_engine import render_template
from src.database.models import TrackingModel
from src.database.repositories import TrackingRepo
from src.gorzdrav_api import GorZdravAPI
from src.gorzdrav_api.exceptions import GorZdravError
from src.gorzdrav_api.schemas import Appointment
from src.gorzdrav_api.utils import filter_appointments
from .storage import StorageProxy

logger = logging.getLogger(__name__)


class TrackingCallback(CallbackData, prefix="tracking"):
    id: int


class AppointmentsChecker:
    def __init__(
            self,
            bot: Bot,
            storage: BaseStorage,
            session_maker: async_sessionmaker
    ) -> None:
        self.bot = bot
        self.storage = storage
        self.session_maker = session_maker

    async def is_notified(
            self,
            tracking: TrackingModel,
            appointments: tuple[Appointment, ...]
    ) -> bool:
        """
        Checks if the notification has already been sent
        """
        storage_proxy = StorageProxy(
            storage=self.storage,
            bot_id=self.bot.id,
            user_id=tracking.user.tg_id
        )

        data = await storage_proxy.get_data()
        last_hash = data.get(tracking.id)
        current_hash = hash(appointments)

        if last_hash and current_hash == last_hash:
            logger.debug(f"Tracking<ID {tracking.id}> "
                         f"notification has already been sent")
            return True

        data[tracking.id] = current_hash
        await storage_proxy.set_data(data=data)
        return False

    async def notify(self, tracking: TrackingModel) -> None:
        """
        Notifies user
        """

        markup_builder = InlineKeyboardBuilder()
        markup_builder.button(
            text=keyboard_texts.checker.SEE_APPOINTMENTS,
            callback_data=TrackingCallback(id=tracking.id).pack()
        )
        await self.bot.send_message(
            chat_id=tracking.user.tg_id,
            text=render_template(
                "tracking/new_appointments.html",
                tracking=tracking
            ),
            reply_markup=markup_builder.as_markup()
        )

        logger.debug(f"Tracking<ID {tracking.id}> notification sent")

    async def check(self, tracking: TrackingModel):
        """
        Gets appointments from API and filters its
        """
        async with GorZdravAPI() as api:
            appointments = await api.get_appointments(
                clinic=tracking.clinic,
                doctor=tracking.doctor,
            )
        filtered_appointments = filter_appointments(
            appointments=appointments,
            hours=tracking.hours
        )

        is_notified = await self.is_notified(
            tracking=tracking,
            appointments=filtered_appointments
        )

        if is_notified:
            return

        if filtered_appointments:
            await self.notify(tracking)

    async def check_all(self) -> None:
        """
        Gets all tracking from database and checks each
        """

        async with self.session_maker() as session:
            repository = TrackingRepo(session=session)
            all_tracking = await repository.get_all_iter(
                order_by=(TrackingModel.clinic, TrackingModel.doctor)
            )

        for tracking in all_tracking:
            with suppress(GorZdravError):
                await self.check(tracking)
