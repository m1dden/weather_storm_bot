import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from bot.handlers import user_commands, callbacks
from bot.config import settings
from bot.utils.scheduler import setup_scheduler

async def main():
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(user_commands.router)
    dp.include_router(callbacks.router)

    # Инициализация планировщика (без указания chat_id)
    setup_scheduler(bot)  # Теперь подписки управляются через storage
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
