import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

import bot_asnwers
from keyboards.inline.profile import action_keyboard, DeleteProfileCallback, confirm_keyboard, ConfirmCallback
from keyboards.reply.profile import generate_profiles_keyboard
from services.database import Repository
from states.profile import ProfileStates, ProfileActionStates

router = Router()
router.callback_query.middleware(CallbackAnswerMiddleware(pre=True))


@router.message(Command("profiles"))
async def profiles_handler(message: types.Message, repository: Repository):
    profiles = await repository.get_user_profiles(message.from_user.id)

    answer_text = ""
    for profile in profiles:
        answer_text += bot_asnwers.PROFILE.format(
            last_name=profile.last_name,
            first_name=profile.first_name,
            middle_name=profile.middle_name,
            birthdate=profile.birthdate.strftime("%d.%m.%Y"),
        )
    if answer_text:
        await message.answer(text=answer_text, reply_markup=action_keyboard)
    else:
        await message.answer(text=bot_asnwers.NO_PROFILES)


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


@router.callback_query(DeleteProfileCallback.filter())
async def delete_profile_handler(callback: types.CallbackQuery, state: FSMContext, repository: Repository):
    profiles = await repository.get_user_profiles(callback.from_user.id)
    keyboard = generate_profiles_keyboard(profiles)

    await state.set_state(ProfileActionStates.select)
    await callback.message.answer(text=bot_asnwers.SELECT_PROFILE, reply_markup=keyboard)


@router.message(ProfileActionStates.select)
async def select_profile_handler(message: types.Message, state: FSMContext, repository: Repository):
    profiles = await repository.get_user_profiles(message.from_user.id)
    selected_profile = next(filter(lambda profile: bot_asnwers.PROFILE_KEYBOARD.format(
        last_name=profile.last_name,
        first_name=profile.first_name,
        middle_name=profile.middle_name,
        birthdate=profile.birthdate.strftime("%d.%m.%Y"),
    ) == message.text, profiles), None)

    if selected_profile:
        await state.update_data(selected_profile=selected_profile)
        await state.set_state(ProfileActionStates.delete_confirm)
        await message.answer(text=bot_asnwers.CONFIRM_DELETE_PROFILE.format(profile=message.text),
                             reply_markup=confirm_keyboard)
    else:
        await message.answer(text=bot_asnwers.UNKNOWN_PROFILE.format(profile=message.text))


@router.callback_query(ProfileActionStates.delete_confirm, ConfirmCallback.filter(F.action == "confirm"))
async def confirm_delete_profile_handler(callback: types.CallbackQuery, state: FSMContext, repository: Repository):
    selected_profile = (await state.get_data())["selected_profile"]
    await repository.delete_profile(selected_profile)

    await state.clear()
    await callback.message.answer(text=bot_asnwers.PROFILE_DELETED)


@router.callback_query(ProfileActionStates.delete_confirm, ConfirmCallback.filter(F.action == "cancel"))
async def cancel_delete_profile_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text=bot_asnwers.DELETE_PROFILE_CANCELED)
