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

@app.route('/')
def index():
    return "Welcome to Svitloe Monitor API. Use /widget to get the status."

def get_light_status():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-application-cache")
        options.add_argument("--incognito")  # Use incognito mode to prevent caching
        options.add_argument("--disable-cache")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("window-size=1920x1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://svitloe.coderak.net/index.html')

        # Wait for the page to load completely
        time.sleep(10)  # Adjust the sleep time if needed

        wait = WebDriverWait(driver, 20)
        status_div = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div')))
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
