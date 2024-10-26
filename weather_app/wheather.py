import requests
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from collections import defaultdict
from datetime import datetime
from pymongo import MongoClient
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

from zeotap.weather_app.models import WeatherAPIData

# MongoDB Setup
MONGO_URI = "mongodb://localhost:27017/"  # Change this to your MongoDB URI
client = MongoClient(MONGO_URI)
db = client['weather_database']
aggregates_collection = db['daily_aggregates']

# API Setup
account_sid = 'AC8200c0799d4e7ac077010a82241b288b'
auth_token = '1e7aaaf17959d5d51a31bba273c98e25'
API_KEY = "f612c3ded24e614595d161735461c06e"
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

# Temperature conversion (Kelvin to Celsius)
def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

# Fetch weather data for a city
def get_weather_data(city):
    url = BASE_URL.format(city, API_KEY)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        main_data = data['main']
        
        return WeatherAPIData(
            city=city,
            weather_condition=data['weather'][0]['main'],
            temp=kelvin_to_celsius(main_data['temp']),
            feels_like=kelvin_to_celsius(main_data['feels_like']),
            timestamp=data['dt']
        )
    else:
        raise ValueError

# Dictionary to hold the daily weather data for each city
weather_summaries = defaultdict(lambda: defaultdict(list))

# Process and store weather data
def process_weather_data():
    for city in CITIES:
        weather_data = get_weather_data(city)
        if weather_data:
            date = datetime.utcfromtimestamp(weather_data['timestamp']).strftime('%Y-%m-%d')
            weather_summaries[city][date].append(weather_data)
            print(f"Weather data for {city} on {date} processed.")

# Function to calculate daily summary
def calculate_daily_summary(weather_data_list):
    total_temp = sum(data['temp'] for data in weather_data_list)
    max_temp = max(data['temp'] for data in weather_data_list)
    min_temp = min(data['temp'] for data in weather_data_list)
    
    dominant_weather = max(set(data['weather'] for data in weather_data_list), key=[data['weather'] for data in weather_data_list].count)
    
    avg_temp = total_temp / len(weather_data_list)
    
    return {
        "average_temp": avg_temp,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "dominant_weather": dominant_weather
    }

# Rollup daily summary and store in MongoDB
def rollup_daily_summary():
    for city, dates in weather_summaries.items():
        for date, weather_data_list in dates.items():
            if weather_data_list:  # Ensure there's data to summarize
                daily_summary = calculate_daily_summary(weather_data_list)
                daily_summary['city'] = city
                daily_summary['date'] = date
                
                # Insert or update the daily aggregate in MongoDB
                aggregates_collection.update_one(
                    {'city': city, 'date': date},
                    {'$set': daily_summary},
                    upsert=True
                )
                
                print(f"Stored daily summary for {city} on {date}: {daily_summary}")

# Dictionary to store alerting thresholds
user_alerts = {
    "temp_threshold": 35  # Example threshold: Alert if temp exceeds 35°C
}

# Function to check thresholds and trigger alerts
def check_thresholds(city, weather_data):
    if weather_data['temp'] > user_alerts['temp_threshold']:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        body=f"ALERT: {city} has exceeded temperature threshold. Temp: {weather_data['temp']}°C",
        from_='+12512782432',
        to='+918000029365'
        )
        print(message.status)

# Monitor for alerts based on threshold
def monitor_alerts():
    for city, dates in weather_summaries.items():
        for date, weather_data_list in dates.items():
            if weather_data_list:
                # Check the last recorded weather data
                check_thresholds(city, weather_data_list[-1])

scheduler = BlockingScheduler()





# Fetch weather data every 1 minute
scheduler.add_job(process_weather_data, 'interval', minutes=1)
# Rollup daily summaries at the end of the day (midnight)
scheduler.add_job(rollup_daily_summary, 'interval', minutes=5)
# Check for alerts every 5 minutes
scheduler.add_job(monitor_alerts, 'interval', minutes=1)

try:
    print("Starting weather monitoring system...")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Weather monitoring system stopped.")
