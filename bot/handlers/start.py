from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот прогноза погоды и магнитных бурь по Самаре 🌦️🌍\n\n"
                         "/weather — Погода\n"
                         "/storm — Магнитные бури")
