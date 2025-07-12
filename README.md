# 🌦️ Weather Storm Bot

Telegram-бот для отслеживания погоды и магнитных бурь с регулярными уведомлениями.  
Бот предоставляет актуальные метеоданные и предупреждает о геомагнитной активности, если уровень превышает заданный порог.


---

## ✨ Возможности

- Прогноз погоды по заданному городу (поддержка OpenWeather API и/или wttr.in)
- Мониторинг уровня магнитных бурь (по данным NOAA)
- Автоматические уведомления каждые 4 часа
- Мгновенные оповещения при повышенной геомагнитной активности
- Удобное управление через inline кнопки Telegram-бота

---

## 🛠️ Стек технологий

- Python 3.10+
- [aiogram 3.x](https://docs.aiogram.dev/) — асинхронная работа с Telegram Bot API
- [httpx](https://www.python-httpx.org/) — асинхронные HTTP-запросы
- [APScheduler](https://apscheduler.readthedocs.io/) — планировщик задач
- [Pydantic](https://docs.pydantic.dev/) + [pydantic-settings](https://pydantic-docs.helpmanual.io/usage/pydantic_settings/)
- Docker + Docker Compose — контейнеризация

---

## 🚀 Установка и запуск

### 🔹 Вариант 1: Локальный запуск

```bash
# Клонировать репозиторий
git clone https://github.com/m1dden/weather_storm_bot.git
cd weather_storm_bot
```
```bash
# Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

```bash
# Установить зависимости
pip install -r requirements.txt
```

```bash
#Создайте файл .env в корне проекта и добавьте:

BOT_TOKEN=your_telegram_bot_token
OPENWEATHER_API_KEY=your_openweather_key
```

```bash
#Запустить бота:

python bot/main.py
```

###🔹 Вариант 2: Запуск через Docker

docker-compose up -d --build



## Автор

Автор проекта **Новаев Денис**
[Telegram](https://t.me/m1dden)

p.s 
Бот уже работает в продакшене и стабильно присылает данные каждые 4 часа.
Хочешь попробовать? Загляни: @NeDayBuri_bot
