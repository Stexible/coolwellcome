import os
import logging
import asyncio
import sys
from typing import Final

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- Настройка Логирования ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Конфигурация ---
# Адаптируем под Bothost: берем токен из переменной или аргумента
BOT_TOKEN: Final[str] = os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or (sys.argv[1] if len(sys.argv) > 1 else None)

if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set.")
    raise ValueError("Missing BOT_TOKEN variable.")

# --- Инициализация Aiogram ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# --- Логика Инлайн-Клавиатуры ---
def get_start_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="Телеграм-канал с новостями",
        url="https://t.me/coolnexart_academy"
    )
    builder.button(
        text="Получить контакт ментора",
        url="https://t.me/coolnex28"
    )
    
    builder.adjust(1) 
    return builder.as_markup()

# --- Обработчик команды /start ---
@router.message(Command("start"))
async def command_start_handler(message: types.Message) -> None:
    welcome_text = (
        "Привет! Я бот coolnexart.online 🎨\n"
        "Я не собираю и не храню ваши личные данные."
    )
    
    await message.answer(
        text=welcome_text,
        reply_markup=get_start_keyboard()
    )

# --- Главная функция запуска (Polling вместо Webhook) ---
async def main():
    dp.include_router(router)
    logger.info("Бот запущен через Polling...")
    # Удаляем вебхук на случай, если он был установлен ранее
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
