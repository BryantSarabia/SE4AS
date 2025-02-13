import os

from src.analyzer import Analyzer
from src.config import Config
from src.user_preferences import UserPreferences

from analyzer import Analyzer

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mqtt://mosquitto:1883')
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', "")

def main():
    config = Config(
        MQTT_BROKER_URL=MQTT_BROKER_URL,
        BACKEND_URL=BACKEND_URL,
        WEATHER_API_KEY=WEATHER_API_KEY
    )
    
    analyzer = Analyzer(config)
    analyzer.run()

if __name__ == "__main__":
    main()