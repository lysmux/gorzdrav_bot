import asyncio
import pickle
from itertools import groupby, chain

from aiogram import Bot, Dispatcher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.gorzdrav.keyboards.inline import remove_tracking_mp
from bot.gorzdrav.keyboards.paginator_items import appointments_items_factory
from bot.utils.inline_paginator import Paginator
from bot.utils.template_engine import render_template
from database.database import Repository
from database.models.tracking import Tracking
from gorzdrav_api.api import GorZdravAPI
from gorzdrav_api.schemas import Appointment


class AppointmentsChecker:
    def __init__(
            self,
            dispatcher: Dispatcher,
            bot: Bot,
            database_pool: async_sessionmaker,
            check_every: int,
            redis: Redis | None = None
    ):
        self.bot = bot
        self.dispatcher = dispatcher
        self.database_pool = database_pool
        self.check_every = check_every

        self.redis = redis
        self.already_notified = {}

    def _is_notified_dict(
            self,
            tracking: Tracking,
            appointments: list[Appointment]
    ):
        if self.already_notified.get(tracking.id) == appointments:
            return True

        self.already_notified[tracking.id] = appointments
        return False

    async def _is_notified_redis(
            self,
            tracking: Tracking,
            appointments: list[Appointment]
    ):
        key = f"appointments_checker:{tracking.id}"
        value = await self.redis.get(key)
        if value:
            last_appointments = pickle.loads(value)
            if last_appointments == appointments:
                return True

        await self.redis.set(key, pickle.dumps(appointments, protocol=pickle.HIGHEST_PROTOCOL))
        return False

    async def is_notified(
            self,
            tracking: Tracking,
            appointments: list[Appointment]
    ):
        if self.redis:
            return await self._is_notified_redis(tracking, appointments)
        else:
            return self._is_notified_dict(tracking, appointments)

    async def check(self):
        async with self.database_pool() as session:
            repository = Repository(session)
            all_tracking = await repository.get_all_tracking()

        grouped_tracking = groupby(all_tracking, key=lambda x: (x.clinic, x.doctor))
        for key, group in grouped_tracking:
            clinic, doctor = key
            async with GorZdravAPI() as api:
                appointments = await api.get_appointments(clinic=clinic, doctor=doctor)

            for tracking in group:
                hours = set(chain.from_iterable((range(*i) for i in tracking.time_ranges)))
                filtered_appointments = list(filter(lambda x: x.time.hour in hours, appointments))

                if filtered_appointments:
                    await self.notify(tracking=tracking, appointments=filtered_appointments)

    async def notify(
            self,
            tracking: Tracking,
            appointments: list[Appointment]
    ):
        if await self.is_notified(tracking, appointments):
            return

        items = appointments_items_factory(
            district=tracking.district,
            clinic=tracking.clinic,
            speciality=tracking.speciality,
            doctor=tracking.doctor,
            appointments=appointments
        )

        paginator = Paginator(
            router=self.dispatcher,
            name="appointments",
            header_text=render_template("gorzdrav/tracking/new_appointments.html", tracking=tracking),
            items=items,
            static_markup=remove_tracking_mp(tracking)
        )

        await paginator.send_paginator_by_bot(bot=self.bot, chat_id=tracking.tg_user_id)

    async def run(self):
        while True:
            await self.check()
            await asyncio.sleep(self.check_every * 60)
