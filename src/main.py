import asyncio
import logging

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from aiogram_dialog.widgets.text.jinja import JINJA_ENV_FIELD

from src.bot.services import AppointmentsChecker
from src.bot.setup import run_as_webhook, run_as_pooling, get_dispatcher
from src.bot.structures import TransferStruct
from src.bot.utils.set_bot_commands import set_bot_commands
from src.bot.utils.template_engine import jinja_env
from src.database import get_engine
from src.settings import Settings

logger = logging.getLogger(__name__)


async def run_bot(settings: Settings):
    engine = get_engine(db_settings=settings.db)
    dispatcher = get_dispatcher(settings=settings)

    # setup bot
    bot = Bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    setattr(bot, JINJA_ENV_FIELD, jinja_env)  # for aio dialogs
    await set_bot_commands(bot)

    # setup aiogram dialogs
    aiod_manager_factory = setup_dialogs(dispatcher)

    # setup appointments checker
    appointments_checker = AppointmentsChecker(
        bot=bot,
        db_engine=engine,
        storage=dispatcher.storage,
        manager_factory=aiod_manager_factory,
        settings=settings
    )

    # run
    async with asyncio.TaskGroup() as tg:
        if settings.use_webhook:
            task = run_as_webhook(
                bot=bot,
                dispatcher=dispatcher,
                transfer_data=TransferStruct(engine=engine),
                webhook_settings=settings.webhook
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
    settings = Settings()  # type: ignore

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        logger.info("GorZdrav bot is running")
        asyncio.run(run_bot(settings=settings))
    except (KeyboardInterrupt, SystemExit):
        logger.info("GorZdrav bot stopped")


if __name__ == "__main__":
    main()
