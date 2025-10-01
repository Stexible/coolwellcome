# Cool Welcome Bot

Это простой Telegram-бот, написанный на Python с использованием библиотек `aiogram` и `fastapi`.

## Функционал

- Приветствует пользователя по команде `/start`.
- Отправляет инлайн-клавиатуру с полезными ссылками.

## Развертывание

Бот предназначен для развертывания в Google Cloud Run.

### Требования

- Установленный [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

### Шаги развертывания

1. **Склонируйте репозиторий:**
   ```bash
   git clone https://github.com/Stexible/cool_wellcome_bot.git
   cd cool_wellcome_bot
   ```

2. **Установите переменные окружения:**
   Вам понадобятся следующие переменные:
   - `TELEGRAM_TOKEN`: Токен вашего Telegram-бота (получается у @BotFather).
   - `WEBHOOK_SECRET`: Случайная секретная строка для защиты вебхука.
   - `WEBHOOK_HOST`: URL вашего сервиса в Cloud Run (станет известен после первого деплоя).

3. **Запустите команду деплоя:**
   ```bash
   gcloud run deploy my-telegram-bot --source . --region <your-region> --set-env-vars=TELEGRAM_TOKEN="<your-token>",WEBHOOK_SECRET="<your-secret>",WEBHOOK_HOST="<your-host>" --allow-unauthenticated
   ```
   Замените `<your-region>`, `<your-token>`, `<your-secret>` и `<your-host>` на ваши реальные значения.
