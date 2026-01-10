from aiogram import Router, F
from aiogram.filters import Command
from aiogram.handlers import CallbackQueryHandler
from aiogram.types import Message, CallbackQuery

from keybords.ikb import IKB

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет, я бот для мониторинга сервера Bozdyrev.Dev\n\n"
                         "Пользуйся меню ниже", reply_markup=IKB.Menu.get_menu())

@router.callback_query(F.data == "back")
async def start(callback: CallbackQuery):
    await callback.message.edit_text("Привет, я бот для мониторинга сервера Bozdyrev.Dev\n\n"
                         "Пользуйся меню ниже", reply_markup=IKB.Menu.get_menu())