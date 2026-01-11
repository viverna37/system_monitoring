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
    await callback.message.edit_text(text="Я создам тебе новую схему и пользователя для нее, чтобы ты мог безопасно работать с базой данной.\n\nПришли мне название схемы, а я сам создам пользователя", reply_markup=IKB.DockerManagement.get_menu())
    await callback.answer()

@router.message(StateFilter("wait_names_schemas"))
async def wait_names(message: Message, state: FSMContext):
    names = message.text
    result = create_schemas(names.strip())
    if result:
        await message.answer("Успешно создал cхему, пользователя и огранчил соответствующие права\n\nДоступ\n"
                             "<blockquote>"
                             "DB_HOST=postgres"
                             f"DB_USER={names+"_user"}"
                             f"DB_PASSWORD=super-strong-password"
                             f"DB_NAME=main_db"
                             f"DB_PORT=5432"
                             "</blockquote>\n\n"
                             "Ничего не урони :)")
        await message.answer("Главное меню", reply_markup=IKB.Menu.get_menu())
    else:
        await message.answer("Sorry caught traceback :)", reply_markup=IKB.Menu.get_menu())

    await state.clear()
