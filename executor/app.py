import os

from src.config import Config
from src.executor import Executor

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mosquitto:1883')

def main():
    config = Config(
        MQTT_BROKER_URL=MQTT_BROKER_URL
    )
    
    executor = Executor(config)
    executor.run()

if __name__ == "__main__":
    main()