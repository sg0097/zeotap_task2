import os
import pandas as pd
import requests
from datetime import datetime
from config import TEMP_THRESHOLD, CITIES, API_KEY

def fetch_weather_forecast(city):
    """
    Fetch weather forecast data for a specific city using OpenWeatherMap API.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

def fetch_forecast_data():
    """
    Retrieve forecast data for all specified cities and save it to a CSV file.
    """
    all_forecast_data = []
    
    for city in CITIES:
        forecast = fetch_weather_forecast(city)
        if forecast:
            all_forecast_data.append({
                'city': city,
                'temp': forecast['main']['temp'],
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed'],
                'main': forecast['weather'][0]['main'],
                'dt': datetime.now()  # Current datetime
            })

    forecast_df = pd.DataFrame(all_forecast_data)

    # Convert the 'dt' column to a formatted date string
    forecast_df['dt'] = forecast_df['dt'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Save to CSV
    forecast_df.to_csv('data/forecast_data.csv', index=False)
    print(f"Forecast data saved to data/forecast_data.csv")
    
    return forecast_df

def calculate_daily_summary(city=None):
    """
    Calculate daily summary for a specific city or for all cities.
    """
    # Load all weather_data CSV files from the data/ directory
    files = [f for f in os.listdir('data') if f.startswith('weather_data')]
    all_data = pd.concat([pd.read_csv(f'data/{file}') for file in files])
    
    if city:
        all_data = all_data[all_data['city'] == city]  # Filter by city if provided

    # Convert 'dt' column to 'date' in datetime format
    all_data['date'] = pd.to_datetime(all_data['dt'], unit='s').dt.date

    # Group by date and city to calculate the daily summary
    summary = all_data.groupby(['date', 'city']).agg(
        avg_temp=('temp', 'mean'),
        max_temp=('temp', 'max'),
        min_temp=('temp', 'min'),
        avg_humidity=('humidity', 'mean'),
        max_humidity=('humidity', 'max'),
        min_humidity=('humidity', 'min'),
        avg_wind_speed=('wind_speed', 'mean'),
        max_wind_speed=('wind_speed', 'max'),
        min_wind_speed=('wind_speed', 'min'),
        dominant_condition=('main', lambda x: x.mode()[0])  # Get most frequent condition
    ).reset_index()

    # Save summary to CSV
    summary_path = 'data/daily_summary.csv'
    summary.to_csv(summary_path, index=False)
    print(f"Summary saved to {summary_path}")  # Confirmation message

    return summary

def check_alerts(df):
    # Iterate through rows and check for temperature alerts
    for index, row in df.iterrows():
        if row['temp'] > TEMP_THRESHOLD:
            print(f"Alert! Temperature in {row['city']} exceeded {TEMP_THRESHOLD}C")

def process_weather_data(city=None):
    # Load all weather_data CSV files from the data/ directory
    files = [f for f in os.listdir('data') if f.startswith('weather_data')]
    all_data = pd.concat([pd.read_csv(f'data/{file}') for file in files])
    
    # Print first few rows of the loaded data for verification
    print("Loaded weather data:")
    print(all_data.head())

    # Calculate the daily summary
    daily_summary = calculate_daily_summary(city)
    
    # Check for temperature alerts
    check_alerts(all_data)

    return daily_summary
