from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot
from bot.utils.keyboards import get_main_menu_keyboard
from bot.utils.scheduler import storage, setup_scheduler

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Брат! 35 бели роз не смогу сделать, но погоду и бурьки покажу.\n"
        "Чего желаешь узнать:",
        reply_markup=get_main_menu_keyboard(
            is_subscribed=message.from_user.id in storage.subscribers
        )
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
async def subscribe(message: Message, bot: Bot):
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
