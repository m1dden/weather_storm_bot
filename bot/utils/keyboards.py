from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_main_menu_keyboard(is_subscribed: bool = False):
    builder = InlineKeyboardBuilder()
    
    # Первый ряд - основные функции
    builder.row(
        InlineKeyboardButton(text="🌤 Погода", callback_data="weather"),
        InlineKeyboardButton(text="🌌 Магнитные бури", callback_data="geomagnetic")
    )
    
    # Второй ряд - управление подпиской
    if is_subscribed:
        builder.row(
            InlineKeyboardButton(text="🔕 Отписаться", callback_data="unsubscribe")
        )
    else:
        builder.row(
            InlineKeyboardButton(text="🔔 Подписаться", callback_data="subscribe")
        )
    
    # Третий ряд - сервисные кнопки
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh"),
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    )
    
    return builder.as_markup()