from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keybords.ikb import IKB
from utils.system import get_system_status, format_uptime

router = Router()

@router.callback_query(F.data == "server_menu")
async def start(callback: CallbackQuery):
    await callback.message.answer("Меню управления сервером", reply_markup=IKB.Server.get_menu())

@router.callback_query(F.data == "system_monitoring")
async def system_status(callback: CallbackQuery):
    s = get_system_status()

    cpu = s["cpu"]
    ram = s["ram"]
    disk = s["disk"]
    net = s["net"]

    text = (
        "🖥 <b>Состояние сервера</b>\n\n"

        "🧠 <b>CPU</b>\n"
        f"• Загрузка: {cpu['percent']}%\n"
        f"• Ядра: {cpu['cores_physical']} / {cpu['cores_logical']}\n"
        f"• Частота: {cpu['freq']:.0f} MHz\n"
        + (f"• Температура: {cpu['temp']}°C\n" if cpu['temp'] else "")
        + "\n"

        "💾 <b>RAM</b>\n"
        f"• {ram['used']:.1f} / {ram['total']:.1f} GB ({ram['percent']}%)\n\n"

        "💽 <b>Disk</b>\n"
        f"• {disk['used']:.1f} / {disk['total']:.1f} GB ({disk['percent']}%)\n\n"

        "🌐 <b>Сеть</b>\n"
        f"• ↑ {net['sent']:.2f} GB\n"
        f"• ↓ {net['recv']:.2f} GB\n\n"

        "📊 <b>Прочее</b>\n"
        f"• Load: {s['load'][0]:.2f} {s['load'][1]:.2f} {s['load'][2]:.2f}\n"
        f"• Процессов: {s['processes']}\n"
        f"• Uptime: {format_uptime(s['uptime'])}"
    )

    await callback.message.answer(text, parse_mode="HTML")
