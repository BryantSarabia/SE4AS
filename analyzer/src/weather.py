import requests
from cachetools import TTLCache, cached

BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

class WeatherFetcher:
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = BASE_URL

    def fetch_weather(self, lat, lon):
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch weather data: {response.status_code}")
            return None
        
    # Cache the weather data for 10 minutes
    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_weather(self, lat, lon):
        return self.fetch_weather(lat, lon)