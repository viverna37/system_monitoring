from aiogram import Router, F

from aiogram.types import CallbackQuery
from keybords.ikb import IKB

router = Router()


@router.callback_query(F.data == "docker_menu")
async def docker_stats(callback: CallbackQuery):
    await callback.message.edit_text(text="Docker menu", reply_markup=IKB.Docker.get_menu())
    await callback.answer()
