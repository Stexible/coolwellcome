#!/bin/bash

# --- Шаг 0: Настройка Переменных Конфигурации ---
# ------------------------------------------------
GCP_PROJECT_ID="storied-visitor-443714-v3"
BOT_TOKEN="8480214986:AAEct0D4Hxkn9QCw3IBYzL0TSq-hmgytRTg"
# ИЗМЕНИТЕ ЭТО ЗНАЧЕНИЕ! Оно должно быть СЛОЖНЫМ и УНИКАЛЬНЫМ.
WEBHOOK_SECRET_VALUE="fe690b52f4eb3c2fd24eb1b12dee1be4cef2728d56cf143770d2e59f954e69d2"
SERVICE_NAME="telegram-webhook-bot"
REGION="us-central1"
REPO_NAME="cloud-run-repo" # Имя репозитория для Docker-образа

# Установка проекта по умолчанию
gcloud config set project $GCP_PROJECT_ID

# Полное имя образа
IMAGE_NAME="${REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}"
echo "--- Начинается сборка и деплой ---"

# --- Шаг 1: Сборка и Публикация Docker-Образа ---
echo "1. Сборка и отправка образа..."

# Создание репозитория Artifact Registry, если он не существует.
# Используется оператор '||' для запуска 'create', если 'describe' завершился ошибкой.
gcloud artifacts repositories describe $REPO_NAME --location=$REGION --format='value(name)' > /dev/null 2>&1 || \
    gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION --description="Docker repository for Cloud Run"

# ИСПРАВЛЕНО: Убрана лишняя точка в конце $IMAGE_NAME
gcloud builds submit --tag $IMAGE_NAME

# Проверка результата сборки
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Сборка образа провалена. Деплой Cloud Run отменен."
    exit 1
fi

# --- Шаг 2: Развертывание Сервиса Cloud Run ---
echo "2. Развертывание сервиса Cloud Run..."

# --allow-unauthenticated необходим, чтобы Telegram мог отправлять запросы [2, 3]
# Передача критических переменных окружения
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --project $GCP_PROJECT_ID \
    --allow-unauthenticated \
    --set-env-vars TELEGRAM_TOKEN="${BOT_TOKEN}",WEBHOOK_SECRET="${WEBHOOK_SECRET_VALUE}" \
    --cpu 1 \
    --memory 512Mi \
    --concurrency 80 \
    --port 8080

# Проверка успеха деплоя
if [ $? -ne 0 ]; then
    echo "КРИТИЧЕСКАЯ ОШИБКА: Деплой Cloud Run провален."
    exit 1
fi

# Получение публичного URL сервиса
CLOUD_RUN_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)')

# ИСПРАВЛЕНО: Проверка, что URL не пуст
if; then
    echo "ОШИБКА: Не удалось получить публичный URL Cloud Run после деплоя."
    exit 1
fi

echo "--- Деплой Cloud Run завершен. Публичный URL: $CLOUD_RUN_URL ---"

# --- Шаг 3: Установка Webhook через Telegram API ---
echo "3. Установка Webhook Telegram API..."
WEBHOOK_PATH="/webhook"
FULL_WEBHOOK_URL="${CLOUD_RUN_URL}${WEBHOOK_PATH}"

# Отправка команды setWebhook в Telegram API
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
    -H "Content-Type: application/json" \
    -d "{
        \"url\": \"${FULL_WEBHOOK_URL}\",
        \"secret_token\": \"${WEBHOOK_SECRET_VALUE}\",
        \"drop_pending_updates\": true
    }"

echo ""
echo "--- Проверьте вывод cURL выше. Ответ должен содержать \"ok\": true ---"

# --- Шаг 4: Проверка Статуса Webhook ---
echo "4. Проверка статуса Webhook..."
curl "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"
