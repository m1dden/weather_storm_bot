import httpx
from bot.config import settings
from bot.utils.keyboards import get_main_menu_keyboard

async def get_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": 53.195873,  # Самара
        "lon": 50.100193,
        "appid": settings.openweather_api_key,
        "units": "metric",
        "lang": "ru"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"].capitalize()
    wind_speed = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]

    weather_text = (
        f"📍 Погода в Самаре:\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"☁️ Облачность: {description}\n"
        f"💨 Ветер: {wind_speed} м/с\n"
        f"💧 Влажность: {humidity}%\n"
        f"🔍 Давление: {pressure} гПа"
    )
    
    return weather_text
