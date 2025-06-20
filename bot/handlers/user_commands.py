# from aiogram import Router, types
# from aiogram.filters import Command
# from aiogram.types import Message
# from aiogram import Bot  # Добавляем импорт Bot
# from bot.utils.keyboards import get_main_menu_keyboard
# from bot.utils.scheduler import setup_scheduler
# from bot.utils.scheduler import storage


# router = Router()

# @router.message(Command("start"))
# async def start(message: types.Message):
#     await message.answer(
#         "Брат! 35 бели роз не смогу сделать, но погоду и бурьки покажу.\n"
#         "Чего желаешь узнать:",
#         reply_markup=get_main_menu_keyboard()
#     )

# @router.message(Command("help"))
# async def help_command(message: types.Message):
#     await message.answer(
#         "📌 Доступные команды:\n"
#         "/start - Главное меню\n"
#         "/weather - Погода в Самаре\n"
#         "/storm - Геомагнитная активность\n\n"
#         "Или используй кнопки ниже:",
#         reply_markup=get_main_menu_keyboard()
#     )

# @router.message(Command("subscribe"))
# async def subscribe(message: Message, bot: Bot):
#     storage.add(message.chat.id)
#     await message.answer("✅ Вы подписаны на обновления!")
#     setup_scheduler(bot)  # Активируем при первой подписке

# @router.message(Command("unsubscribe"))
# async def unsubscribe(message: Message):
#     storage.remove(message.chat.id)
#     await message.answer("❌ Вы отписались от рассылки")

# @router.message(Command("admin"))
# async def admin_command(message: Message):
#     if message.from_user.id != settings.admin_id:
#         await message.answer("❌ Команда только для админа")
#         return
#     # ... админские действия ...

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot  # Добавляем импорт Bot
from bot.utils.keyboards import get_main_menu_keyboard
from bot.utils.scheduler import storage, setup_scheduler  # Четкий импорт нужных объектов

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Брат! 35 бели роз не смогу сделать, но погоду и бурьки покажу.\n"
        "Чего желаешь узнать:",
        reply_markup=get_main_menu_keyboard()
    )

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📌 Доступные команды:\n"
        "/start - Главное меню\n"
        "/weather - Погода в Самаре\n"
        "/storm - Геомагнитная активность\n"
        "/subscribe - Подписаться на уведомления\n"
        "/unsubscribe - Отписаться от уведомлений\n\n"
        "Или используй кнопки ниже:",
        reply_markup=get_main_menu_keyboard()
    )

@router.message(Command("subscribe"))
async def subscribe(message: Message, bot: Bot):  # Теперь Bot распознается
    storage.add(message.chat.id)
    setup_scheduler(bot)
    await message.answer(
        "✅ Вы подписаны на регулярные обновления!",
        reply_markup=get_main_menu_keyboard()
    )

@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):
    storage.remove(message.chat.id)
    await message.answer(
        "❌ Вы отписались от рассылки",
        reply_markup=get_main_menu_keyboard()
    )