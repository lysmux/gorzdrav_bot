import datetime

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import bot_asnwers
from profile.states import ProfileStates
from services.database import Repository

router = Router()


@router.message(Command("create_profile"))
async def create_profile_handler(message: types.Message, state: FSMContext):
    await state.set_state(ProfileStates.last_name)
    await message.answer(text=bot_asnwers.CREATE_PROFILE)
    await message.answer(text=bot_asnwers.ENTER_LAST_NAME)


@router.message(ProfileStates.last_name, F.text)
async def last_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(ProfileStates.first_name)
    await message.answer(text=bot_asnwers.ENTER_FIRST_NAME)


@router.message(ProfileStates.first_name, F.text)
async def first_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(ProfileStates.middle_name)
    await message.answer(text=bot_asnwers.ENTER_MIDDLE_NAME)


@router.message(ProfileStates.middle_name, F.text)
async def middle_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(middle_name=message.text)
    await state.set_state(ProfileStates.birthdate)
    await message.answer(text=bot_asnwers.ENTER_BIRTHDATE)


@router.message(ProfileStates.birthdate, F.text)
async def birthdate_handler(message: types.Message, state: FSMContext, repository: Repository):
    try:
        birthdate = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer(text=bot_asnwers.WRONG_DATE)
        return
    await state.update_data(birthdate=birthdate)

    profile_data = await state.get_data()
    await repository.create_profile(
        tg_user_id=message.from_user.id,
        last_name=profile_data["last_name"],
        first_name=profile_data["first_name"],
        middle_name=profile_data["middle_name"],
        birthdate=profile_data["birthdate"],
    )

    await state.clear()
    await message.answer(text=bot_asnwers.PROFILE_CREATED)
