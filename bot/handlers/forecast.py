from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.weather import get_weather
from bot.services.geomagnetic import get_geomagnetic_data

router = Router()

@router.message(Command("weather"))
async def weather_handler(message: Message):
    forecast = await get_weather()
    await message.answer(f"Погода в Самаре:\n{forecast}")

@router.message(Command("storm"))
async def storm_handler(message: Message):
    storm = await get_geomagnetic_data()
    await message.answer(f"Магнитные бури:\n{storm}")
