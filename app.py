from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Svitloe Monitor API. Use /widget to get the status."

def get_light_status():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://svitloe.coderak.net/index.html')

        wait = WebDriverWait(driver, 10)
        status_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="status"]')))
        status_text = status_div.text
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)
        status_text = f"Error: {str(e)}"
    finally:
        driver.quit()
    
    return status_text

@app.route('/widget')
def widget():
    status_text = get_light_status()
    return jsonify({"status_text": status_text})

if __name__ == '__main__':
    app.run(debug=True)
