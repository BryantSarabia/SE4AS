import json
import os
import time

import paho.mqtt.client as mqtt
from src.zone import ZoneService

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mosquitto:1883')
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000')

def parse_mqtt_url(url):
    parts = url.split(":")
    host = parts[0]
    port = int(parts[1]) if len(parts) > 1 else 1883
    return host, port

class SensorSimulator:
    def __init__(self, mqtt_broker_url, mqtt_port, backend_url):
        self.zone_service = ZoneService(backend_url)
        self.backend_url = backend_url
        self.zones = []
        self.load_zones()

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.connect(mqtt_broker_url, mqtt_port, 60)
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        self.simulate_sensor_data()

    def load_zones(self):
        try:
          zones = self.zone_service.get_zones()
          self.zones = zones
        except Exception as e:
          print(f"Error loading zones: {e}")

    def simulate_sensor_data(self):
        while True:
            for zone in self.zones:
                for field in zone.fields:
                    for sensor in field.get_all_sensors():
                        value = sensor.simulate_value()
                        topic = f"zone/{zone.zone_id}/field/{field.field_id}/sensor/{sensor.sensor_id}/{sensor.type.value}"
                        message = json.dumps({'value': value})
                        self.mqtt_client.publish(topic, message)
                        print(f"Published sensor data: Zone={zone.zone_id}, Field={field.field_id}, Sensor={sensor.sensor_id}, Type={sensor.type.value}, Value={value}")
            time.sleep(10)  # Simulate data every 10 seconds

if __name__ == "__main__":
    host, port = parse_mqtt_url(MQTT_BROKER_URL)
    simulator = SensorSimulator(host, port, BACKEND_URL)
