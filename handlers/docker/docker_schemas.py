from email.errors import MessageDefect

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message
from keybords.ikb import IKB
from utils.docker_create_schemas import create_schemas

router = Router()


@router.callback_query(F.data == "docker_management")
async def docker_stats(callback: CallbackQuery):
    await callback.message.edit_text(text="Docker menu", reply_markup=IKB.DockerManagement.get_menu())
    await callback.answer()

@router.callback_query(F.data == "create_schemas")
async def docker_stats(callback: CallbackQuery, state: FSMContext):
    await state.set_state("wait_names_schemas")

    await callback.message.edit_text(text="Введи имя схема и имя пользователя через enter", reply_markup=IKB.DockerManagement.get_menu())
    await callback.answer()

@router.message(StateFilter("wait_names_schemas"))
async def wait_names(message: Message, state: FSMContext):
    names = message.text.split("\n")
    result = create_schemas(*names)
    if result:
        await message.answer("Успешно создал cхему, пользователя и огранчил соответствующие права")
    else:
        await message.answer("Sorry caught traceback :)")

    await state.clear()