from pydantic import BaseModel
from typing import List

class WeatherSummary(BaseModel):
    min_temp:float
    max_temp:float
    avg_temp:float
    weather_conditions: List[str]
    dominant_weather: str
    iteration: int

class WeatherData(WeatherSummary):
    city: str = None
    date: str = None
    
class WeatherAPIData(BaseModel):
    city:str
    temp:float
    feels_like:float
    weather_condition:str
    timestamp: int

