import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import routers
from config import load_config


from tasks.temperature_alerts import TemperatureMonitor



async def main():
    config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(routers)


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
