from aiogram import Router, types
from aiogram.filters import Command
from bot.utils.keyboards import get_main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот, который показывает погоду и геомагнитную активность.\n"
        "Выбери действие:",
        reply_markup=get_main_menu_keyboard()
    )

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📌 Доступные команды:\n"
        "/start - Главное меню\n"
        "/weather - Погода в Самаре\n"
        "/storm - Геомагнитная активность\n\n"
        "Или используй кнопки ниже:",
        reply_markup=get_main_menu_keyboard()
    )
