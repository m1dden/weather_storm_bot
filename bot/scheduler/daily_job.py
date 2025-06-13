from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.services.weather import get_weather
from bot.services.geomagnetic import get_geomagnetic_data
from aiogram import Bot


async def send_daily_forecast(bot: Bot, chat_id: int):
    weather = await get_weather()
    storm = await get_geomagnetic_data()
    text = f"Доброе утро! Вот прогноз на сегодня ☀️\n\n{weather}\n\n{storm}"
    await bot.send_message(chat_id=chat_id, text=text)


def setup_scheduler(bot: Bot, chat_id: int):
    scheduler = AsyncIOScheduler(timezone="Europe/Samara")
    scheduler.add_job(send_daily_forecast, "cron", hour=7, minute=0, args=[bot, chat_id])
    scheduler.start()
