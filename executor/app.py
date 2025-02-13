import os

from src.executor import Executor

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mqtt://mosquitto')

if __name__ == "__main__":
    executor = Executor(MQTT_BROKER_URL)