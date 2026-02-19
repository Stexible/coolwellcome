import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters


# Хостинг Bothost обычно передает токен аргументом или через переменную
TOKEN = os.getenv("BOT_TOKEN") or (sys.argv[1] if len(sys.argv) > 1 else None)

# текст приветствия
WELCOME_TEXT = (
    "👋 Привет!\n\n"
    "Я — бот сайта coolnexart.online.\n\n"
    "ℹ️ Я не собираю и не храню никакие личные данные пользователей.\n\n"
    "Если вы хотите записаться на обучение или задать вопрос преподавателю, "
    "пожалуйста, свяжитесь напрямую с ним: 👉 @coolnex28\n\n"
    "💬 Напишите преподавателю, и он лично расскажет вам обо всех деталях."
)

async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text(WELCOME_TEXT)

async def any_message(update, context):
    """Обработчик любых сообщений"""
    await update.message.reply_text(WELCOME_TEXT)

def main():
    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))
    # все остальные сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, any_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

