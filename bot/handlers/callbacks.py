from aiogram import Router, types, F
from datetime import datetime
from bot.services.cache import data_cache
from bot.utils.keyboards import get_main_menu_keyboard


router = Router()

def add_timestamp(text: str) -> str:
    """Добавляет временную метку к сообщению"""
    if text and "🔄 Обновлено:" in text:
        return f"{text.split('🔄 Обновлено:')[0].strip()}\n\n🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"
    return f"{text or 'Нет данных'}\n\n🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"

@router.callback_query(F.data == "weather")
async def weather_callback(callback: types.CallbackQuery):
    try:
        weather_text = await data_cache.get_weather()
        updated_text = add_timestamp(weather_text)
        await callback.message.edit_text(
            text=updated_text,
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer("Данные из кэша" if data_cache.is_cached("weather") else "Новые данные получены")
    except Exception as e:
        await callback.answer(f"⚠️ Ошибка: {e}", show_alert=True)

@router.callback_query(F.data == "geomagnetic")
async def geomagnetic_callback(callback: types.CallbackQuery):
    try:
        geomagnetic_text = await data_cache.get_geomagnetic_data()  # Используем новый метод
        updated_text = add_timestamp(geomagnetic_text)
        await callback.message.edit_text(
            text=updated_text,
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer("Данные из кэша" if data_cache.is_cached("geomagnetic") else "Новые данные получены")
    except Exception as e:
        await callback.answer(f"⚠️ Ошибка: {e}", show_alert=True)

@router.callback_query(F.data == "refresh")
async def refresh_callback(callback: types.CallbackQuery):
    try:
        if "Погода" in callback.message.text:
            # Принудительное обновление
            data_cache.force_expire("weather")
            new_data = await data_cache.get_weather()
        elif "Геомагнитная" in callback.message.text:
            data_cache.force_expire("geomagnetic")
            new_data = await data_cache.get_geomagnetic_data()
        else:
            await callback.answer("❌ Нельзя обновить это сообщение", show_alert=True)
            return
        
        updated_text = add_timestamp(new_data)
        await callback.message.edit_text(
            text=updated_text,
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer("🔄 Данные принудительно обновлены")
    except Exception as e:
        await callback.answer(f"⚠️ Ошибка: {e}", show_alert=True)

@router.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    try:
        await callback.message.edit_text(
            "📌 Доступные команды:\n"
            "/start - Главное меню\n"
            "/weather - Погода в Самаре\n"
            "/storm - Геомагнитная активность\n"
            "/subscribe - Подписаться на уведомления\n"
            "/unsubscribe - Отписаться от уведомлений\n\n"
            "Или используй кнопки ниже:",
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer()
    except Exception as e:
        await callback.answer(f"⚠️ Ошибка: {e}", show_alert=True)
