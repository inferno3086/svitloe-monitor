# Базовый образ Python
FROM python:3.9-slim

# Установить необходимые зависимости
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    && apt-get clean

# Установить Google Chrome
RUN wget -q -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i /tmp/google-chrome.deb || apt-get -fy install \
    && rm /tmp/google-chrome.deb

# Проверить версию Chrome
RUN google-chrome --version

# Скопировать ваш ChromeDriver версии 131 в образ
COPY ./chromedriver /usr/local/bin/chromedriver



# Сделать ChromeDriver исполняемым
RUN chmod +x /usr/local/bin/chromedriver

# Установить Python-зависимости
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать код приложения
COPY . /app

# Открыть порт и запустить приложение
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
