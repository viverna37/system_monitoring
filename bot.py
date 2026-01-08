import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from handlers.system_status import router as system_status
from handlers.docker_status import router as docker_status
from handlers.docker_stats import router as docker_stats
from tasks.temperature_alerts import TemperatureMonitor


async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(system_status)
    dp.include_router(docker_status)
    dp.include_router(docker_stats)

    temp_monitor = TemperatureMonitor(
        warn=75,
        critical=85,
        interval=30,
    )

    asyncio.create_task(
        temp_monitor.run(bot, config.tg_bot.admin_ids)
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
