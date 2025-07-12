# 🌦️ Weather Storm Bot

**Telegram-бот для отслеживания погоды и магнитных бурь с регулярными уведомлениями.**  
Бот предоставляет актуальные метеоданные и предупреждает о геомагнитной активности, если уровень превышает заданный порог.

---

## ✨ Возможности

- 📍 Прогноз погоды по заданному городу (поддержка OpenWeather API и/или [wttr.in](https://wttr.in))
- 🌐 Мониторинг магнитных бурь (по данным [NOAA](https://www.swpc.noaa.gov/))
- 🕓 Автоматические уведомления каждые 4 часа
- ⚠️ Мгновенные оповещения при повышенной геомагнитной активности
- 🤖 Удобное управление через inline-кнопки Telegram-бота

---

## 🛠️ Стек технологий

- Python 3.10+
- [aiogram 3.x](https://docs.aiogram.dev/) — асинхронная работа с Telegram Bot API
- [httpx](https://www.python-httpx.org/) — асинхронные HTTP-запросы
- [APScheduler](https://apscheduler.readthedocs.io/) — планировщик задач
- [Pydantic](https://docs.pydantic.dev/) и [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — валидация и управление конфигурацией
- Docker + Docker Compose — контейнеризация

---

## 🚀 Установка и запуск

### 🔹 Вариант 1: Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/m1dden/weather_storm_bot.git
cd weather_storm_bot
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate        # для Linux/macOS
venv\Scripts\activate           # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта и добавьте в него:
```env
BOT_TOKEN=your_telegram_bot_token
OPENWEATHER_API_KEY=your_openweather_key
```

5. Запустите бота:
```bash
python bot/main.py
```

---

### 🔹 Вариант 2: Запуск через Docker

1. Соберите и запустите контейнер:
```bash
docker-compose up -d --build
```

---

## 🧑‍💻 Автор

**Новаев Денис**  
[Telegram: @m1dden](https://t.me/m1dden)

> 💡 Бот уже работает в продакшене и стабильно присылает данные каждые 4 часа.  
> Хочешь попробовать? Загляни: [@NeDayBuri_bot](https://t.me/NeDayBuri_bot)
