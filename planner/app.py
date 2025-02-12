import os

from .src.planner import Planner

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mqtt://mosquitto')

if __name__ == "__main__":
    planner = Planner(MQTT_BROKER_URL)