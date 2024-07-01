from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

app = Flask(__name__)

def get_light_status():
    url = "https://svitloe.coderak.net/index.html"
    
    # Настройка Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Ожидание загрузки динамического контента
    driver.implicitly_wait(10)
    
    # Извлечение текста
    status_div = driver.find_element(By.XPATH, '/html/body/header/div/div')
    status_text = status_div.text.strip()
    
    driver.quit()

    # Отладочные выводы
    print("Status Text:", status_text)  # Печать извлеченного текста для отладки

    return {
        "text": status_text
    }

@app.route('/widget', methods=['GET'])
def widget():
    return jsonify(get_light_status())

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the light status API. Go to /widget to see the status."

if __name__ == "__main__":
    app.run(debug=True)
