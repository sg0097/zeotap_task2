import pandas as pd
import matplotlib.pyplot as plt

def plot_daily_summary_and_alerts(temp_threshold=35):
    # Load daily summary data
    df = pd.read_csv('data/daily_summary.csv')
    df['date'] = pd.to_datetime(df['date'])

    # Plot Temperature Summary
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['avg_temp'], label='Average Temperature', color='orange')
    plt.plot(df['date'], df['max_temp'], label='Maximum Temperature', color='red')
    plt.plot(df['date'], df['min_temp'], label='Minimum Temperature', color='blue')
    
    # Highlight alerts in red
    alert_data = df[df['max_temp'] > temp_threshold]
    plt.scatter(alert_data['date'], alert_data['max_temp'], color='red', zorder=5, label=f'Alert > {temp_threshold}C')
    
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Daily Temperature Summary with Alerts')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot Humidity Summary
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['avg_humidity'], label='Average Humidity', color='purple')
    plt.plot(df['date'], df['max_humidity'], label='Maximum Humidity', color='green')
    plt.plot(df['date'], df['min_humidity'], label='Minimum Humidity', color='cyan')
    
    plt.xlabel('Date')
    plt.ylabel('Humidity (%)')
    plt.title('Daily Humidity Summary')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot Wind Speed Summary
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['avg_wind_speed'], label='Average Wind Speed', color='brown')
    plt.plot(df['date'], df['max_wind_speed'], label='Maximum Wind Speed', color='orange')
    plt.plot(df['date'], df['min_wind_speed'], label='Minimum Wind Speed', color='grey')
    
    plt.xlabel('Date')
    plt.ylabel('Wind Speed (m/s)')
    plt.title('Daily Wind Speed Summary')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Run the function to visualize daily summaries and alerts
plot_daily_summary_and_alerts()
