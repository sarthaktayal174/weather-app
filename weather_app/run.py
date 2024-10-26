import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient
from twilio.rest import Client
from config import *
from data_store import WeatherDataStore
from processor import WeatherDataProcessor

weather_api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
wheather_api_key: str = os.getenv("wheather_api_key")
twilio_api_sid: str = os.getenv("twilio_api_sid")
twilio_api_token: str = os.getenv("twilio_api_token")
mongo_host: str = os.getenv("mongo_host")
notification_number = os.getenv("notification_number")
weather_db_name: str = "weather_database"
weather_collection: str = "daily_aggregates"

print(wheather_api_key)

db_client = MongoClient(mongo_host)
data_store = WeatherDataStore(db_client=db_client, db_name=weather_db_name, coll_name=weather_collection)
twilio_client = Client(twilio_api_sid,twilio_api_token)
weather_processor = WeatherDataProcessor(
    base_url=weather_api_url,
    api_key=wheather_api_key,
    data_store=data_store,
    twilio_client=twilio_client,
    alert_threshold = 35,
    notification_number= notification_number
)

scheduler = BlockingScheduler()

# Fetch weather data every 5 minute
scheduler.add_job(weather_processor.run_processor, 'interval', minutes=5)

try:
    print("Starting weather monitoring system...")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Weather monitoring system stopped.")
