import os
import json
import logging
from typing import Set, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from bot.services.cache import data_cache
from bot.utils.keyboards import get_main_menu_keyboard
from bot.config import settings

__all__ = ['storage', 'setup_scheduler']

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubscriberStorage:
    """Класс для хранения и управления подписчиками"""
    def __init__(self, default_ids: Optional[Set[int]] = None):
        self._default_ids = default_ids or {settings.admin_id}
        os.makedirs("data", exist_ok=True)
        self._file_path = "data/subscribers.json"
        self._subscribers = self._load_initial_data()

    @property
    def subscribers(self) -> Set[int]:
        """Текущий список подписчиков"""
        return self._subscribers

    def _load_initial_data(self) -> Set[int]:
        """Загрузка данных из файла или использование значений по умолчанию"""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.info(f"Используем подписчиков по умолчанию: {e}")
            return self._default_ids

    def add(self, chat_id: int) -> None:
        """Добавление нового подписчика"""
        if chat_id not in self._subscribers:
            self._subscribers.add(chat_id)
            self._save_data()

    def remove(self, chat_id: int) -> None:
        """Удаление подписчика"""
        if chat_id in self._subscribers:
            self._subscribers.remove(chat_id)
            self._save_data()

    def _save_data(self) -> None:
        """Сохранение данных в файл"""
        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(list(self._subscribers), f, ensure_ascii=False, indent=2)

# Инициализация компонентов
storage = SubscriberStorage()
scheduler = AsyncIOScheduler()

# async def _send_message_safely(bot: Bot, chat_id: int, text: str) -> bool:
#     """Безопасная отправка сообщения с обработкой ошибок"""
#     try:
#         await bot.send_message(
#             chat_id,
#             text,
#             reply_markup=get_main_menu_keyboard(is_subscribed=chat_id in storage.subscribers)
#         )
#         return True
#     except Exception as e:
#         logger.error(f"Ошибка отправки сообщения для {chat_id}: {e}")
#         if "chat not found" in str(e).lower():
#             storage.remove(chat_id)
#         return False

# async def send_regular_updates(bot: Bot) -> None:
#     """Регулярная рассылка обновлений подписчикам"""
#     weather = await data_cache.get_weather()
#     storms, kp_index = await data_cache.get_geomagnetic_data()
    
#     message_text = (
#         f"🌦 Регулярный прогноз (Kp: {kp_index}):\n\n"
#         f"{weather}\n\n"
#         f"{storms}"
#     )
    
#     for chat_id in list(storage.subscribers):
#         await _send_message_safely(bot, chat_id, message_text)

# async def check_storm_alerts(bot: Bot) -> None:
#     """Проверка и уведомления о магнитных бурях"""
#     _, kp_index = await data_cache.get_geomagnetic_data()
    
#     if kp_index >= 4:
#         alert_text = (
#             f"⚠️ Внимание! Магнитная буря (Kp: {kp_index})!\n\n"
#             "Рекомендуется:\n"
#             "- Снизить физическую активность\n"
#             "- Пить больше воды\n"
#             "- Избегать стрессов"
#         )
        
#         for chat_id in list(storage.subscribers):
#             await _send_message_safely(bot, chat_id, alert_text)


async def _send_message_safely(bot: Bot, chat_id: int, text: str) -> bool:
    """Безопасная отправка сообщения с HTML-форматированием"""
    try:
        await bot.send_message(
            chat_id,
            text,
            parse_mode="HTML",
            reply_markup=get_main_menu_keyboard(is_subscribed=chat_id in storage.subscribers)
        )
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки для {chat_id}: {e}")
        if "chat not found" in str(e).lower():
            storage.remove(chat_id)
        return False

async def send_regular_updates(bot: Bot) -> None:
    """Регулярная рассылка с HTML-форматированием"""
    weather = await data_cache.get_weather()
    storms, kp_index = await data_cache.get_geomagnetic_data()
    
    message_text = (
        f"🌦 <b>Регулярный прогноз</b> (Kp: {kp_index:.1f})\n\n"
        f"{weather}\n\n"
        f"{storms}"
    )
    
    for chat_id in list(storage.subscribers):
        await _send_message_safely(bot, chat_id, message_text)

async def check_storm_alerts(bot: Bot) -> None:
    """Уведомления о бурях с HTML-форматированием"""
    _, kp_index = await data_cache.get_geomagnetic_data()
    
    if kp_index >= 4:
        alert_text = (
            f"⚠️ <b>МАГНИТНАЯ БУРЯ!</b> ⚠️ (Kp: {kp_index:.1f})\n\n"
            "📌 <i>Рекомендации:</i>\n"
            "• Снизить физическую активность\n"
            "• Пить больше воды\n"
            "• Избегать стрессов"
        )
        
        for chat_id in list(storage.subscribers):
            await _send_message_safely(bot, chat_id, alert_text)


def setup_scheduler(bot: Bot) -> None:
    """Настройка и запуск планировщика задач"""
    if scheduler.running:
        logger.warning("Планировщик уже запущен")
        return
    
    scheduler.add_job(
        send_regular_updates,
        'interval',
        hours=4,
        kwargs={'bot': bot},
        id='regular_updates'
    )
    
    scheduler.add_job(
        check_storm_alerts,
        'interval',
        minutes=30,
        kwargs={'bot': bot},
        id='storm_alerts'
    )
    
    try:
        scheduler.start()
        logger.info("Планировщик успешно запущен")
    except Exception as e:
        logger.error(f"Ошибка запуска планировщика: {e}")
