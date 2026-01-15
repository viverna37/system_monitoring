from aiogram import F, Router
from aiogram.types import CallbackQuery

from keybords.ikb import IKB
from utils.docker_monitor import docker_available, get_containers, format_timedelta

router = Router()

@router.callback_query(F.data == "docker_monitoring")
async def docker_status(callback: CallbackQuery):
    if not docker_available():
        await callback.message.answer("❌ Docker daemon недоступен")
        return

    containers = get_containers()

    running = sum(1 for c in containers if c["status"] == "running")
    exited = len(containers) - running

    text = (
        "🐳 <b>Docker status</b>\n\n"
        f"📦 Всего контейнеров: {len(containers)}\n"
        f"🟢 Running: {running}\n"
        f"🔴 Not running: {exited}\n\n"
    )

    for c in containers:
        status_icon = "🟢" if c["status"] == "running" else "🔴"
        text += (
            f"{status_icon} <b>{c['name']}</b>\n"
            f"• status: {c['status']}\n"
            f"• image: {c['image']}\n"
            f"• uptime: {format_timedelta(c['uptime'])}\n\n"
        )

    await callback.message.edit_text(text, reply_markup=IKB.Back.get_menu())
    await callback.answer()