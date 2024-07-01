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

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "Welcome to Svitloe Monitor API. Use /widget to get the status."

def get_light_status():
    status_text = ""
    start_time = time.time()
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-application-cache")
        options.add_argument("--incognito")
        options.add_argument("--disable-cache")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("window-size=1920x1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get('https://svitloe.coderak.net/index.html')

        logging.info("Loading URL: https://svitloe.coderak.net/index.html")
        
        # Wait for the page to load completely
        time.sleep(10)  # Adjust the sleep time if needed

        logging.info("Page loaded, waiting for status element")

        wait = WebDriverWait(driver, 30)  # Increase wait time
        status_div = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div')))
        status_text = status_div.text
        logging.info(f"Extracted status text: {status_text}")
    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)
        status_text = f"Error: {str(e)}"
    finally:
        driver.quit()
    
    end_time = time.time()
    logging.info(f"Execution time: {end_time - start_time} seconds")
    return status_text

@app.route('/widget')
def widget():
    status_text = get_light_status()
    return jsonify({"status_text": status_text})

if __name__ == '__main__':
    app.run(debug=True)
