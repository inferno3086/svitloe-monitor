from flask import Flask, jsonify
from requests_html import HTMLSession
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_light_status():
    url = "https://svitloe.coderak.net/index.html"
    session = HTMLSession()
    response = session.get(url)
    response.html.render()
    soup = BeautifulSoup(response.html.html, 'html.parser')
    status_div = soup.select_one("body > header > div > div")
    status_text = status_div.get_text(strip=True)
    
    if "світло є" in status_text:
        widget_color = "green"
        widget_text = "Свет есть"
    elif "світла нема" in status_text:
        widget_color = "red"
        widget_text = "Света нет"
    else:
        widget_color = "gray"
        widget_text = "Неизвестно"
    
    return {
        "color": widget_color,
        "text": widget_text
    }

@app.route('/widget', methods=['GET'])
def widget():
    return jsonify(get_light_status())

if __name__ == "__main__":
    app.run(debug=True)
