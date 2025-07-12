from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from aiogram import Bot
from datetime import datetime
from bot.utils.keyboards import get_main_menu_keyboard
from bot.utils.scheduler import storage
from bot.services.cache import data_cache


router = Router()

def add_timestamp(text: str) -> str:
    """Функция добавления временной метки"""
    if "🔄 Обновлено:" in text:
        return f"{text.split('🔄 Обновлено:')[0].strip()}\n\n🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"
    return f"{text}\n\n🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"

@router.callback_query(F.data == "weather")
async def weather_callback(callback: CallbackQuery):
    weather_text = await data_cache.get_weather()
    updated_text = add_timestamp(weather_text)
    await callback.message.edit_text(
        text=updated_text,
        reply_markup=get_main_menu_keyboard(is_subscribed=callback.from_user.id in storage.subscribers)
    )
    await callback.answer()

@router.callback_query(F.data == "geomagnetic")
async def geomagnetic_callback(callback: CallbackQuery):
    geomagnetic_text, kp_index = await data_cache.get_geomagnetic_data()
    updated_text = add_timestamp(geomagnetic_text)
    await callback.message.edit_text(
        text=updated_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard(is_subscribed=callback.from_user.id in storage.subscribers)
    )
    await callback.answer()

@router.callback_query(F.data == "subscribe")
async def subscribe_callback(callback: CallbackQuery, bot: Bot):
    storage.add(callback.from_user.id)
    await callback.message.edit_reply_markup(
        reply_markup=get_main_menu_keyboard(is_subscribed=True)
    )
    await callback.answer("✅ Вы подписаны на обновления")

@router.callback_query(F.data == "unsubscribe")
async def unsubscribe_callback(callback: CallbackQuery):
    storage.remove(callback.from_user.id)
    await callback.message.edit_reply_markup(
        reply_markup=get_main_menu_keyboard(is_subscribed=False)
    )
    await callback.answer("❌ Вы отписались от рассылки")

@router.callback_query(F.data == "refresh")
async def refresh_callback(callback: CallbackQuery):
    try:
        if "Погода" in callback.message.text:
            new_data = await data_cache.get_weather()
        elif "Геомагнитная" in callback.message.text:
            new_data, _ = await data_cache.get_geomagnetic_data()
        else:
            await callback.answer("❌ Нельзя обновить это сообщение", show_alert=True)
            return
        
        updated_text = add_timestamp(new_data)
        await callback.message.edit_text(
            text=updated_text,
            parse_mode="HTML",
            reply_markup=get_main_menu_keyboard(
                is_subscribed=callback.from_user.id in storage.subscribers
            )
        )
        await callback.answer("🔄 Данные обновлены")
    except Exception as e:
        await callback.answer(f"⚠️ Ошибка: {e}", show_alert=True)

@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📌 Доступные команды:\n"
        "/start - Главное меню\n"
        "/weather - Погода в Самаре\n"
        "/storm - Геомагнитная активность\n"
        "/subscribe - Подписаться на уведомления\n"
        "/unsubscribe - Отписаться от уведомлений\n\n"
        "Или используй кнопки ниже:",
        reply_markup=get_main_menu_keyboard(
            is_subscribed=callback.from_user.id in storage.subscribers
        )
    )
    await callback.answer()
