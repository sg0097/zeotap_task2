from flask import Flask, render_template, request, jsonify
from data_retrieval import fetch_weather_data, schedule_data_retrieval
from data_processing import process_weather_data
from threading import Timer

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    # Fetch daily summary for the specified city
    try:
        daily_summary = process_weather_data(city)
        return render_template('weather.html', summary=daily_summary)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Error fetching weather data", 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    # Fetch and return current weather data for all cities
    weather_data = fetch_weather_data()
    return jsonify(weather_data)

@app.route('/api/daily_summary/<city>', methods=['GET'])
def get_daily_summary(city):
    try:
        # Implement logic to retrieve daily summary for the specified city
        daily_summary = process_weather_data(city)
        return jsonify(daily_summary.to_dict(orient='records'))
    except Exception as e:
        print(f"Error fetching daily summary for {city}: {e}")
        return jsonify({"error": str(e)}), 500

def schedule_daily_processing():
    """
    Schedule daily processing of weather data.
    This function will call process_weather_data() once every 24 hours.
    """
    process_weather_data()  # Consider returning processed data if necessary
    Timer(86400, schedule_daily_processing).start()  # 24 hours in seconds

if __name__ == '__main__':
    # Start data retrieval process
    print("Starting the weather data retrieval process...")
    schedule_data_retrieval()  # Ensure this function continuously fetches data

    # Start daily processing
    print("Starting the daily weather data processing schedule...")
    schedule_daily_processing()

    # Run the Flask application
    app.run(host='0.0.0.0', port=8080, debug=True)
