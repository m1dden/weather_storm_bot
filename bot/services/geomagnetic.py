import httpx
from datetime import datetime

NOAA_API_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

async def get_geomagnetic_data() -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NOAA_API_URL)
            response.raise_for_status()
            data = response.json()

        # Берём последнюю запись с наличием kp_index
        latest = next((item for item in reversed(data) if "kp_index" in item), None)

        if latest is None:
            return "⚠️ Данные о геомагнитной активности временно недоступны."

        kp_index = latest["kp_index"]
        time_tag = latest["time_tag"]
        dt = datetime.fromisoformat(time_tag).strftime("%d.%m.%Y %H:%M")

        # Описание уровня активности по шкале
        if kp_index < 3:
            level = "Гуляй, шальная"
        elif kp_index < 5:
            level = "Пупупупу, плохи наши дела..."
        elif kp_index < 7:
            level = "Нам пиздец люда, нам пиздец..."
        else:
            level = "Для такого мема еще не придумали..."

        return (
            f"🌌 Геомагнитная активность:\n"
            f"📊 Индекс Kp: {kp_index}\n"
            f"🕒 Время: {dt}\n"
            f"📈 Уровень: {level}"
        )

    except Exception as e:
        # Можно добавить логирование ошибки при желании
        return "⚠️ Данные о геомагнитной активности временно недоступны."
