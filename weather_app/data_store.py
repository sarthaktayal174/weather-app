from pymongo import MongoClient
from models import WeatherData, WeatherSummary


class WeatherDataStore:
    def __init__(self, db_client: MongoClient, db_name, coll_name):
        self.db_client = db_client
        self.weather_db_name = db_name
        self.weather_collection = coll_name
    
    def get_collection(self, city):
        return self.db_client[self.weather_db_name][f"{self.weather_collection}_{city}"]
    
    def insert_data_in_db(self, data: WeatherData):
        summary = WeatherSummary(**data.dict())
        self.get_collection(data.city).update_one({'date': data.date}, {'$set': summary.dict()},upsert=True)

    def get_weather_data(self, date, city):
        filter = {'date': date}
        res = self.get_collection(city=city).find_one({'date': date})
        return WeatherData(**res, city=city) if res else None

    def get_all_data(self, city):
        res = self.get_collection(city=city).find({})
        data = []
        for row in res:
            row_data = WeatherData(**row, city=city)
            data.append(row_data)
        return data
