import html

from aiogram import Router, F

from aiogram.types import CallbackQuery, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from keybords.ikb import IKB, LogsCb
from utils.docker_management_containers import get_containers, format_timedelta, get_container_by_name, \
    reboot_container, get_container_logs

router = Router()
LOGS_CACHE: dict[str, list[str]] = {}


@router.callback_query(F.data == "containers")
async def docker_stats(callback: CallbackQuery):
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


@router.callback_query(F.data.startswith("card:"))
async def open_card(callback: CallbackQuery):
    name = callback.data.split(":")[1]
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

    await callback.message.edit_text(f"Docker card for {name} container\n",
                                     reply_markup=IKB.DockerManagement.get_management_menu(name))


@router.callback_query(F.data.startswith("reboot:"))
async def open_card(callback: CallbackQuery):
    name = callback.data.split(":")[1]
    ok = reboot_container(name)
    if ok:
        await callback.message.answer(f"Контейнер {name} успешно перезапущен")
    else:
        await callback.message.answer("Sorry caught traceback :(")


@router.callback_query(F.data.startswith("logs:"))
async def open_card(callback: CallbackQuery):
    name = callback.data.split(":")[1]

    pages = get_container_logs(name, limit=900)
    if not pages:
        await callback.answer("Логи пустые")
        return

    LOGS_CACHE[name] = pages

    await callback.message.edit_text(
        text=f"<pre>{pages[0]}</pre>",
        parse_mode="HTML",
        reply_markup=IKB.DockerManagement.logs_pagination_kb(
            name=name,
            page=0,
            total=len(pages)
        )
    )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(LogsCb.filter())
async def paginate_logs(
        callback: CallbackQuery,
        callback_data: LogsCb,
):
    name = callback_data.name
    page = callback_data.page

    pages = LOGS_CACHE.get(name)
    if not pages:
        await callback.answer("Логи устарели", show_alert=True)
        return

    page = max(0, min(page, len(pages) - 1))
    new_text = f"<pre>{pages[page]}</pre>"

    if callback.message.text == new_text:
        await callback.answer("Дальше нельзя")
        return

    await callback.message.edit_text(
        text=f"<pre>{html.escape(pages[0])}</pre>",
        parse_mode="HTML",
        reply_markup=IKB.DockerManagement.logs_pagination_kb(
            name=name,
            page=0,
            total=len(pages)
        )
    )
    await callback.answer()
