import asyncio
import logging

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from aiogram_dialog.widgets.text.jinja import JINJA_ENV_FIELD

from bot import run_as_webhook, run_as_pooling, get_dispatcher
from bot.services import AppointmentsChecker
from bot.structures import TransferStruct
from bot.utils.set_bot_commands import set_bot_commands
from bot.utils.template_engine import jinja_env
from config import settings
from database import get_engine

logger = logging.getLogger("main")


async def run_bot():
    engine = get_engine()
    dispatcher = get_dispatcher()

    # setup bot
    bot = Bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    setattr(bot, JINJA_ENV_FIELD, jinja_env)  # for aio dialogs
    await set_bot_commands(bot)

    # setup aiogram dialogs
    aiod_manager_factory = setup_dialogs(dispatcher)

    # setup appointments checker
    appointments_checker = AppointmentsChecker(
        bot=bot,
        manager_factory=aiod_manager_factory,
        storage=dispatcher.storage,
        db_engine=engine,
        check_every=settings.check_every,
    )

    # run
    async with asyncio.TaskGroup() as tg:
        if settings.use_webhook:
            task = run_as_webhook(
                bot=bot,
                dispatcher=dispatcher,
                transfer_data=TransferStruct(engine=engine)
            )
        else:
            task = run_as_pooling(
                bot=bot,
                dispatcher=dispatcher,
                transfer_data=TransferStruct(engine=engine)
            )

        tg.create_task(task)
        tg.create_task(appointments_checker.run())


def main() -> None:
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        logger.info("GorZdrav bot is running")
        asyncio.run(run_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.info("GorZdrav bot stopped")


if __name__ == "__main__":
    main()
