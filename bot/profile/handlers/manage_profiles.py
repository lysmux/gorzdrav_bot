from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot import bot_asnwers
from bot.profile.keyboards.inline import ConfirmCallback, confirm_keyboard, DeleteProfileCallback, action_keyboard
from bot.profile.keyboards.reply import generate_profiles_keyboard
from bot.profile.states import ProfileActionStates
from database.database import Repository

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
