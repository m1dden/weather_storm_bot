from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from bot.services.weather import get_weather
from bot.services.geomagnetic import get_geomagnetic_data
from bot.utils.keyboards import get_main_menu_keyboard

router = Router()

# Обработчик кнопки "Погода"
@router.callback_query(F.data == "weather")
async def weather_callback(callback: types.CallbackQuery):
    weather = await get_weather()
    await callback.message.edit_text(
        weather,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

# Обработчик кнопки "Магнитные бури"
@router.callback_query(F.data == "geomagnetic")
async def geomagnetic_callback(callback: types.CallbackQuery):
    geomagnetic = await get_geomagnetic_data()
    await callback.message.edit_text(
        geomagnetic,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

# Обработчик кнопки "Помощь"
@router.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📌 Доступные команды:\n"
        "/start - Главное меню\n"
        "/weather - Погода в Самаре\n"
        "/storm - Геомагнитная активность\n\n"
        "Или используй кнопки ниже:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()