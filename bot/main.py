# import asyncio
# from aiogram import Bot, Dispatcher
# from bot.config import settings
# from bot.handlers import start, forecast
# from bot.scheduler.daily_job import setup_scheduler


# async def main():
#     bot = Bot(token=settings.bot_token)
#     dp = Dispatcher()
#     dp.include_routers(start.router, forecast.router)

#     # Рассылка одному чату (например, тебе)
#     your_chat_id = 468134766
#     setup_scheduler(bot, your_chat_id)

#     await dp.start_polling(bot)

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from bot.handlers import user_commands, callbacks
from bot.config import settings

async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(user_commands.router)
    dp.include_router(callbacks.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
