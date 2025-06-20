from datetime import datetime, timedelta
from bot.services.weather import get_weather as fetch_weather
from bot.services.geomagnetic import get_geomagnetic_data as fetch_geomagnetic

class DataCache:
    def __init__(self):
        self.cache = {
            "weather": {
                "data": None,
                "timestamp": None,
                "expires_in": timedelta(minutes=10)  # Кэш на 10 минут
            },
            "geomagnetic": {
                "data": None,
                "timestamp": None,
                "expires_in": timedelta(minutes=30)  # Кэш на 30 минут
            }
        }

    async def get_weather(self):
        return await self._get_data("weather", fetch_weather)

    async def get_geomagnetic_data(self):
        return await self._get_data("geomagnetic", fetch_geomagnetic)

    async def _get_data(self, data_type, fetch_function):
        cache_entry = self.cache[data_type]
        
        # Если данные в кэше актуальны - возвращаем их
        if cache_entry["data"] and datetime.now() - cache_entry["timestamp"] < cache_entry["expires_in"]:
            return cache_entry["data"]
        
        # Получаем новые данные
        new_data = await fetch_function()
        self.cache[data_type] = {
            "data": new_data,
            "timestamp": datetime.now(),
            "expires_in": cache_entry["expires_in"]
        }
        return new_data

    def is_cached(self, data_type):
        """Проверяет, используются ли кэшированные данные"""
        cache_entry = self.cache.get(data_type)
        if not cache_entry or not cache_entry["data"]:
            return False
        return datetime.now() - cache_entry["timestamp"] < cache_entry["expires_in"]

    def force_expire(self, data_type):
        """Принудительно делает кэш неактуальным"""
        if data_type in self.cache:
            self.cache[data_type]["timestamp"] = datetime.now() - timedelta(days=1)

# Создаем глобальный экземпляр кэша
data_cache = DataCache()
