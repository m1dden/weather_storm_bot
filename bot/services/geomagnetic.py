import httpx
from datetime import datetime
from typing import Tuple  # Добавляем новый импорт

NOAA_API_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

async def get_geomagnetic_data() -> Tuple[str, float]:
    """Возвращает текст сообщения и числовое значение Kp-индекса"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NOAA_API_URL)
            response.raise_for_status()
            data = response.json()

        # Берём последнюю запись с наличием kp_index
        latest = next((item for item in reversed(data) if "kp_index" in item), None)

        if latest is None:
            return "⚠️ Данные о геомагнитной активности временно недоступны.", 0.0

        kp_index = float(latest["kp_index"])
        time_tag = latest["time_tag"]
        dt = datetime.fromisoformat(time_tag).strftime("%d.%m.%Y %H:%M")

        # Определяем уровень активности
        if kp_index < 3:
            level = "Гуляй, шальная"
            emoji = "🟢"
        elif kp_index < 5:
            level = "Пупупупу, плохи наши дела..."
            emoji = "🟡"
        elif kp_index < 7:
            level = "Нам пиздец люда, нам пиздец..."
            emoji = "🔴"
        else:
            level = "Для такого мема еще не придумали..."
            emoji = "⚠️💀⚠️"

        # Формируем сообщение с выделением бури
        message = (
            f"{emoji} <b>Геомагнитная активность</b> {emoji}\n"
            f"📊 <b>Индекс Kp:</b> <code>{kp_index}</code>\n"
            f"🕒 <b>Время:</b> {dt}\n"
            f"📈 <b>Уровень:</b> {level}"
        )

        # Добавляем предупреждение если буря
        if kp_index >= 4:
            message = (
                f"⚠️ <b>МАГНИТНАЯ БУРЯ!</b> ⚠️\n\n"
                f"{message}\n\n"
                f"<i>Рекомендуется снизить физическую активность</i>"
            )

        return message, kp_index

    except Exception as e:
        # Логирование ошибки можно добавить здесь
        return "⚠️ Данные о геомагнитной активности временно недоступны.", 0.0