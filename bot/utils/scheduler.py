__all__ = ['storage', 'setup_scheduler']
import os
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from bot.services.cache import data_cache
from bot.utils.keyboards import get_main_menu_keyboard
from bot.config import settings

class SubscriberStorage:
    def __init__(self, default_ids=None):
        if default_ids is None:
            default_ids = {settings.admin_id}
        
        os.makedirs("data", exist_ok=True)
        self.file_path = "data/subscribers.json"
        self.subscribers = self._load(default_ids)
    
    def _load(self, default_ids):
        try:
            with open(self.file_path) as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return default_ids
    
    def add(self, chat_id: int):
        if chat_id not in self.subscribers:
            self.subscribers.add(chat_id)
            self._save()
    
    def remove(self, chat_id: int):
        if chat_id in self.subscribers:
            self.subscribers.remove(chat_id)
            self._save()
    
    def _save(self):
        with open(self.file_path, 'w') as f:
            json.dump(list(self.subscribers), f)

# Инициализация после определения класса
storage = SubscriberStorage()
scheduler = AsyncIOScheduler()

async def send_regular_updates(bot: Bot):
    """Рассылка всем подписчикам"""
    weather = await data_cache.get_weather()
    storms, kp_index = await data_cache.get_geomagnetic_data()
    
    for chat_id in storage.subscribers:
        try:
            await bot.send_message(
                chat_id,
                f"🌦 Регулярный прогноз (Kp: {kp_index}):\n\n{weather}\n\n{storms}",
                reply_markup=get_main_menu_keyboard()
            )
        except Exception as e:
            print(f"Ошибка отправки для {chat_id}: {e}")

async def check_storm_alerts(bot: Bot):
    """Проверка и уведомления о бурях"""
    _, kp_index = await data_cache.get_geomagnetic_data()
    
    if kp_index >= 4:
        for chat_id in storage.subscribers:
            try:
                await bot.send_message(
                    chat_id,
                    f"⚠️ Внимание! Магнитная буря (Kp: {kp_index})!\n"
                    "Рекомендуется снизить физическую активность.",
                    reply_markup=get_main_menu_keyboard()
                )
            except Exception as e:
                print(f"Ошибка уведомления для {chat_id}: {e}")

def setup_scheduler(bot: Bot):
    """Инициализация планировщика"""
    if not scheduler.running:
        scheduler.add_job(
            send_regular_updates,
            'interval',
            hours=4,
            kwargs={'bot': bot}
        )
        scheduler.add_job(
            check_storm_alerts,
            'interval',
            minutes=30,
            kwargs={'bot': bot}
        )
        scheduler.start()
