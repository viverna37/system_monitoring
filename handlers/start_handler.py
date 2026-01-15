from aiogram import Router, F
from aiogram.filters import Command
from aiogram.handlers import CallbackQueryHandler
from aiogram.types import Message, CallbackQuery

from keybords.ikb import IKB
from utils.docker_management_containers import get_containers
from utils.docker_monitor import format_timedelta

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет, я бот для мониторинга сервера Bozdyrev.Dev\n\n"
                         "Пользуйся меню ниже", reply_markup=IKB.Menu.get_menu())

@router.callback_query(F.data == "exit")
async def start(callback: CallbackQuery):
    await callback.message.edit_text("Привет, я бот для мониторинга сервера Bozdyrev.Dev\n\n"
                         "Пользуйся меню ниже", reply_markup=IKB.Menu.get_menu())

@router.callback_query(F.data == "exit_2")
async def start(callback: CallbackQuery):
    containers = get_containers()

    text = (
        "<b>Docker containers management</b>\n\n"
        f"📦 Всего контейнеров: {len(containers)}\n"
    )

    for c in containers:
        status_icon = "🟢" if c["status"] == "running" else "🔴"
        text += (
            f"{status_icon} <b>{c['name']}</b>\n"
            f"• uptime: {format_timedelta(c['uptime'])}\n\n"
        )

    await callback.message.edit_text(text=text, reply_markup=IKB.DockerManagement.get_containers_keyboard(containers))
    await callback.answer()
