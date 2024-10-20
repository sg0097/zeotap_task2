import requests
import pandas as pd
from datetime import datetime
from threading import Timer
from config import API_KEY, CITIES, INTERVAL

def fetch_weather_data(city=None):
    """
    Fetch current weather data for a specific city or for all cities if city is None.
    """
    if city:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'city': city,
                'main': data['weather'][0]['main'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'dt': data['dt']
            }
            return weather_info
        else:
            print(f"Error fetching data for {city}: {response.status_code}")
            return None
    else:
        # Fetch data for all cities
        all_weather_data = []
        for city in CITIES:
            data = fetch_weather_data(city)
            if data:
                all_weather_data.append(data)
        return all_weather_data  # Return list of all cities' weather data

def fetch_and_store_data():
    """
    Fetch weather data for all cities and store it in a CSV file.
    """
    all_weather_data = fetch_weather_data()  # Fetch all cities data
    if all_weather_data:
        df = pd.DataFrame(all_weather_data)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        df.to_csv(f'data/weather_data_{timestamp}.csv', index=False)
        print(f"Data fetched and stored at {timestamp}")
    else:
        print("No data to store.")

def schedule_data_retrieval():
    """
    Schedule the fetching and storing of weather data at defined intervals.
    """
    fetch_and_store_data()
    Timer(INTERVAL, schedule_data_retrieval).start()

# Start the data retrieval process
schedule_data_retrieval()
