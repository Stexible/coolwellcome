import os
import logging
from typing import Final, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message, Update
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- Настройка Логирования ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Конфигурация из переменных окружения ---
BOT_TOKEN: Final[str] = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET: Final[str] = os.getenv("WEBHOOK_SECRET")
WEBHOOK_HOST: Final[str] = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH: Final[str] = "/webhook" # Можно вынести в переменную окружения, если нужно

if not all([BOT_TOKEN, WEBHOOK_SECRET, WEBHOOK_HOST]):
    logger.error("Critical environment variables are not set (TELEGRAM_TOKEN, WEBHOOK_SECRET, WEBHOOK_HOST).")
    raise ValueError("Missing critical environment variables.")

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# --- Инициализация Aiogram ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# --- Логика Инлайн-Клавиатуры ---
def get_start_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Телеграм-канал с новостями", url="https://t.me/coolnexart_academy")
    builder.button(text="Получить контакт ментора", url="https://t.me/coolnex28")
    builder.adjust(1)
    return builder.as_markup()

# --- Обработчик команды /start ---
@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    welcome_text = (
        "Привет! Я бот coolnexart.online 🎨\n"
        "Я не собираю и не храню ваши личные данные."
    )
    await message.answer(text=welcome_text, reply_markup=get_start_keyboard())

# --- Lifespan для управления Webhook ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
        logger.info(f"Webhook set to {WEBHOOK_URL}")
    else:
        logger.info("Webhook is already set.")
    yield
    logger.info("Shutting down...")
    await bot.delete_webhook()
    logger.info("Webhook deleted.")

# --- Инициализация FastAPI и Webhook Эндпоинт ---
app = FastAPI(lifespan=lifespan)
dp.include_router(router)

@app.post(WEBHOOK_PATH)
async def main_handler(
    request_data: dict[str, Any],
    x_telegram_bot_api_secret_token: str | None = Header(default=None)
):
    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        logger.warning("Unauthorized webhook attempt.")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid Secret Token")

    telegram_update = Update.model_validate(request_data)
    await dp.feed_update(bot, telegram_update)
    return {"message": "OK"}

@app.get("/")
def root():
    return {"status": "ok"}