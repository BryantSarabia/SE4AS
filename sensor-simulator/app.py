import json
import logging
import os
import time
from typing import Tuple

import paho.mqtt.client as mqtt
from src.zone import ZoneService

# Configuration
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mosquitto:1883')
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000')

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _parse_mqtt_url(url: str) -> Tuple[str, int]:
    parts = url.split(":")
    host = parts[0]
    port = int(parts[1])
    return host, port

class SensorSimulator:
    def __init__(self, mqtt_broker_url, mqtt_port, backend_url):
        logger.info(f"MQTT Broker URL: {mqtt_broker_url}, MQTT Port: {mqtt_port}")
        self.zone_service = ZoneService(backend_url)
        self.backend_url = backend_url
        self.zones = []
        self.load_zones()

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_log = self.on_log

        try:
            self.mqtt_client.connect(mqtt_broker_url, mqtt_port, 60)
            self.mqtt_client.loop_start()
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT broker with result code {rc}")
        else:
            logger.error(f"Failed to connect to MQTT broker with result code {rc}")

    def on_log(self, client, userdata, paho_log_level, messages):
        if paho_log_level == mqtt.LogLevel.MQTT_LOG_ERR:
            print(messages)

    def on_disconnect(self, client, userdata, rc):
        logger.info(f"Disconnected from MQTT broker with result code {rc}")

    def load_zones(self):
        try:
            zones = self.zone_service.get_zones()
            self.zones = zones
        except Exception as e:
            logger.error(f"Error loading zones: {e}")

    def simulate_sensor_data(self):
        logger.info("Starting Sensor Simulator")
        while True:
            for zone in self.zones:
                for field in zone.fields.values():
                    for sensor in field.get_all_sensors():
                        value = sensor.simulate_value()
                        topic = f"zone/{zone.zone_id}/field/{field.field_id}/sensor/{sensor.sensor_id}/{sensor.type}"
                        logger.info(f"Publishing sensor data to topic: {topic}")
                        message = json.dumps({'value': value})
                        try:
                            self.mqtt_client.publish(topic, message)
                            logger.info(f"Published sensor data: Zone={zone.zone_id}, Field={field.field_id}, Sensor={sensor.sensor_id}, Type={sensor.type}, Value={value}")
                        except Exception as e:
                            logger.error(f"Failed to publish sensor data: {e}")
            time.sleep(10)  # Simulate data every 10 seconds

    def stop(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

if __name__ == "__main__":
    host, port = _parse_mqtt_url(MQTT_BROKER_URL)
    simulator = SensorSimulator(host, port, BACKEND_URL)
    simulator.simulate_sensor_data()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     logger.info("Stopping Sensor Simulator")
    #     simulator.stop()
