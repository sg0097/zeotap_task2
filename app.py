from flask import Flask, render_template, request
import pandas as pd
from src.data_retrieval import fetch_weather_data

app = Flask(__name__)

# Route to home with city search
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch city weather data
@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    data = fetch_weather_data(city)
    return render_template('weather.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
