from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def get_light_status():
    url = "https://svitloe.coderak.net/index.html"
    
    logging.info("Starting Selenium WebDriver setup...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = os.getenv('GOOGLE_CHROME_BIN', '/app/.apt/usr/bin/google-chrome')
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    logging.info("Navigating to URL: %s", url)
    driver.get(url)
    
    driver.implicitly_wait(10)
    
    try:
        status_div = driver.find_element(By.XPATH, '/html/body/header/div/div')
        status_text = status_div.text.strip()
        logging.info("Status Text Extracted: %s", status_text)
    except Exception as e:
        logging.error("Error while finding element: %s", e)
        status_text = "Error retrieving status"
    
    driver.quit()
    
    if "світло є" in status_text:
        widget_color = "green"
        widget_text = "Свет есть"
    else:
        widget_color = "red"
        widget_text = "Света нет"
    
    return {
        "color": widget_color,
        "text": widget_text
    }

@app.route('/widget', methods=['GET'])
def widget():
    return jsonify(get_light_status())

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the light status API. Go to /widget to see the status."

if __name__ == "__main__":
    app.run(debug=True)
