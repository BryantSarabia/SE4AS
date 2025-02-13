import os

from .src.analyzer import Analyzer
from .src.user_preferences import UserPreferences

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mqtt://mosquitto:1883')
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000')


if __name__ == "__main__":
    analyzer = Analyzer(MQTT_BROKER_URL, BACKEND_URL, UserPreferences)
    analyzer.run()