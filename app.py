from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Svitloe Monitor API. Use /widget to get the status."

async def get_light_status():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://svitloe.coderak.net/index.html')

    try:
        wait = WebDriverWait(driver, 10)
        status_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="status-text"]')))
        status_text = status_div.text
    except Exception as e:
        status_text = "Error: {}".format(e)
    finally:
        driver.quit()
    
    return status_text

@app.route('/widget')
def widget():
    status_text = asyncio.run(get_light_status())
    return jsonify({"status_text": status_text})

if __name__ == '__main__':
    app.run(debug=True)
