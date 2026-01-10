import logging

from aiogram import Router, F

from aiogram.types import CallbackQuery, InlineKeyboardButton

import docker
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keybords.ikb import IKB
from utils.docker_management_containers import get_containers, format_timedelta, get_container_by_name

router = Router()


@router.callback_query(F.data == "containers")
async def docker_stats(callback: CallbackQuery):
    containers = get_containers()

    running = sum(1 for c in containers if c["status"] == "running")
    exited = len(containers) - running

    text = (
        "<b>Docker containers management</b>\n\n"
        f"📦 Всего контейнеров: {len(containers)}\n"
    )

    for c in containers:
        status_icon = "🟢" if c["status"] == "running" else "🔴"
        text += (
            f"{status_icon} <b>{c['name']}</b>\n"
            f"• status: {c['status']}\n"
            f"• uptime: {format_timedelta(c['uptime'])}\n\n"
        )

    keybord = InlineKeyboardBuilder()
    for i in containers:
        keybord.add(InlineKeyboardButton(text=i['image'], callback_data=f"card_{i['name']}"))
    keybord.add(InlineKeyboardButton(text="Назад", callback_data="back_2"))
    keybord.adjust(1)
    await callback.message.edit_text(text=text, reply_markup=keybord.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("card_"))
async def open_card(callback: CallbackQuery):
    name = callback.data.split("_")[1]
    logging.Logger(name, level=logging.WARNING)
    c = get_container_by_name(name)
    await callback.answer()
    text = ""
    status_icon = "🟢" if c["status"] == "running" else "🔴"
    text += (
        f"id: {c['id']}\n"
        f"{status_icon} <b>{c['name']}</b>\n"
        f"• status: {c['status']}\n"
        f"• uptime: {format_timedelta(c['uptime'])}\n\n"
    )


    await callback.message.answer("Docker card\n", reply_markup=IKB.DockerManagement.get_management_menu(name))
