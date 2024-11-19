FROM python:3.9-slim

# Установить рабочую директорию
WORKDIR /app

# Скопировать файлы проекта
COPY . /app

# Установить зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указать порт
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]
