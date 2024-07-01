from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def get_light_status():
    url = "https://svitloe.coderak.net/index.html"
    
    # Настройка Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    logging.info("Starting WebDriver")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    logging.info("WebDriver started successfully")
    
    driver.get(url)
    logging.info("URL loaded: %s", url)
    
    try:
        # Ожидание загрузки динамического контента
        wait = WebDriverWait(driver, 30)  # Увеличенное время ожидания
        status_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="status-text"]')))
        status_text = status_div.text.strip()
        logging.info("Extracted text using Selenium: %s", status_text)
    except Exception as e:
        logging.error("Error extracting text with Selenium: %s", e)
        status_text = "Error retrieving status"
    
    driver.quit()
    
    return {
        "status_text": status_text
    }

@app.route('/widget', methods=['GET'])
def widget():
    return jsonify(get_light_status())

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the light status API. Go to /widget to see the status."

if __name__ == "__main__":
    app.run(debug=True)
