# Используем официальный slim-образ Python 3.11+
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# 1. Установка всех зависимостей напрямую (без requirements.txt) [2, 3]
RUN pip install --no-cache-dir \
    "aiogram>=3.4.1" \
    "fastapi>=0.111.0" \
    "uvicorn[standard]>=0.30.1"

# Копируем исходный код приложения
COPY bot.py /app/bot.py

# Cloud Run требует прослушивания переменной окружения PORT, по умолчанию 8080.
ENV PORT 8080
EXPOSE 8080

# Команда запуска Uvicorn для Cloud Run [4]
CMD uvicorn bot:app --host 0.0.0.0 --port $PORT
