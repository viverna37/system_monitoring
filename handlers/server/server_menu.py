from aiogram import Router, F
from aiogram.types import CallbackQuery

from keybords.ikb import IKB

router = Router()

@router.callback_query(F.data == "server_menu")
async def start(callback: CallbackQuery):
    await callback.message.edit_text("Меню управления сервером", reply_markup=IKB.Server.get_menu())

