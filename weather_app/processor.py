from datetime import datetime
import requests

from data_store import WeatherDataStore
from models import WeatherAPIData, WeatherData, WeatherSummary
from config import CITIES
from twilio.rest import Client


class WeatherDataProcessor:
    def __init__(self, base_url, api_key, data_store: WeatherDataStore, twilio_client: Client, alert_threshold, notification_number:str) -> None:
        self.api_url = base_url
        self.api_key = api_key
        self.data_store = data_store
        self.alert_threshold = alert_threshold
        self.twilio_client = twilio_client
        self.notification_number = notification_number
    
    def kelvin_to_celsius(self, kelvin_temp):
        return kelvin_temp - 273.15

    def get_weather_data(self, city):
        url = self.api_url.format(city, self.api_key)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            main_data = data['main']
            
            return WeatherAPIData(
                city=city,
                weather_condition=data['weather'][0]['main'],
                temp=self.kelvin_to_celsius(main_data['temp']),
                feels_like=self.kelvin_to_celsius(main_data['feels_like']),
                timestamp=data['dt']
            )
        else:
            raise ValueError
    
    def check_alert_threshold(self, weather_data: WeatherAPIData):
        if weather_data.temp > self.alert_threshold:
            message = self.twilio_client.messages.create(
                body=f"ALERT: {weather_data.city} has exceeded temperature threshold. Temp: {weather_data['temp']}°C",
                from_='+12512782432',
                to=self.notification_number
            )
    
    
    def create_weather_data(self, data: WeatherAPIData, date: str):
        return  WeatherSummary(
            min_temp=data.temp,
            max_temp=data.temp,
            avg_temp=data.temp,
            weather_conditions = [data.weather_condition],
            dominant_weather = data.weather_condition,
            iteration = 1,
            city = data.city,
            date = date
        )
    
    def update_weather_summary(self, data: WeatherAPIData,date:str,summary:WeatherSummary):
        return  WeatherData(
            min_temp=min(data.temp,summary.min_temp),
            max_temp=max(data.temp,summary.max_temp),
            avg_temp=(((summary.iteration*summary.avg_temp)+data.temp)/(summary.iteration +1)),
            weather_conditions = summary.weather_conditions + [data.weather_condition],
            dominant_weather = max(set(data for data in summary.weather_conditions), key=[data for data in summary.weather_conditions].count),
            iteration = summary.iteration + 1,
            city = data.city,
            date = date
        )
        
    def update_weather_data(self, data: WeatherAPIData):
        date = datetime.fromtimestamp(data.timestamp).strftime('%Y-%m-%d')
        weather_data = self.data_store.get_weather_data(date=date, city=data.city)
        if weather_data:
            data_with_latest_summary = self.update_weather_summary(data, date, weather_data)
        else:
            data_with_latest_summary = self.create_weather_data(data,date)
        self.data_store.insert_data_in_db(data_with_latest_summary)

    
    def run_processor(self):
        for city in CITIES:
            weather_data = self.get_weather_data(city)
            self.update_weather_data(weather_data)
            self.check_alert_threshold(weather_data)

        