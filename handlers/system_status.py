from aiogram import Router
from aiogram.types import Message
from utils.system import get_system_status

router = Router()

def format_uptime(seconds: int) -> str:
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m"

@router.message()
async def status_handler(message: Message):
    stats = get_system_status()

    text = (
        "🖥 <b>Состояние сервера</b>\n\n"
        f"CPU: <b>{stats['cpu']}%</b>\n"
        f"RAM: <b>{stats['ram']}%</b>\n"
        f"Disk: <b>{stats['disk']}%</b>\n"
        f"Load: {stats['load'][0]:.2f} "
        f"{stats['load'][1]:.2f} "
        f"{stats['load'][2]:.2f}\n"
        f"Uptime: {format_uptime(stats['uptime'])}"
    )

    await message.answer(text, parse_mode="HTML")
