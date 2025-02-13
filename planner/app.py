import os

from src.config import Config
from src.planner import Planner

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mqtt://mosquitto')

def main():
    config = Config(
        MQTT_BROKER_URL=MQTT_BROKER_URL
    )
    
    planner = Planner(config)
    planner.run()

if __name__ == "__main__":
    main()