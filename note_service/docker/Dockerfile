# Используем официальный образ Python (slim версия)
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты
COPY note_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY note_service/ note_service/

# Запускаем приложение как модуль, добавляя /app в sys.path
CMD ["python", "-m", "note_service.app.main"]
