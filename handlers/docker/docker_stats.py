from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.docker_stats import get_docker_stats, format_mem, bytes_to_mb

router = Router()


@router.callback_query(F.data == "docker_stats")
async def docker_stats(callback: CallbackQuery):
    stats = get_docker_stats()

    if not stats:
        await callback.message.answer("🐳 Docker запущен, но контейнеров нет")
        return

    text = "🐳 <b>Docker stats</b>\n\n"

    for s in stats:
        text += (
            f"🟢 <b>{s['name']}</b>\n"
            f"CPU: {s['cpu']}%\n"
            f"RAM: {format_mem(s['mem_used'], s['mem_limit'])}\n"
            f"NET: ↓ {bytes_to_mb(s['net_rx']):.1f} MB "
            f"↑ {bytes_to_mb(s['net_tx']):.1f} MB\n\n"
        )

    await callback.message.edit_text(text)
    await callback.answer()
