from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

app = Flask(__name__)

# Настроим логирование
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "Welcome to Svitloe Monitor API. Use /widget to get the status."

@app.route('/widget', methods=['GET'])
def widget():
    try:
        status_text = get_light_status()
        return jsonify(status_text=status_text)
    except Exception as e:
        logging.error(f"Error in /widget route: {e}")
        return jsonify(status_text="Error occurred"), 500

def get_light_status():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    try:
        logging.info("Loading URL")
        driver.get('https://svitloe.coderak.net/index.html')

        logging.info("Waiting for element")
        status_div = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div')))
        logging.info("Element found")
        status_text = status_div.text
        logging.info(f"Extracted text: {status_text}")
    except Exception as e:
        logging.error(f"Error in get_light_status: {e}")
        status_text = "Error occurred"
    finally:
        driver.quit()
    
    return status_text

if __name__ == '__main__':
    app.run(debug=True)
