import json
import logging
import os
import random
from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread
from typing import Tuple

import paho.mqtt.client as mqtt

from .actuator import ActuatorType

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mosquitto:1883')
CONSUMPTION_TOPIC = 'zone/{zone_id}/field/{field_id}/actuator/+/+/consumption'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SensorType(Enum):
    SOIL_MOISTURE = 'soil_moisture'
    LIGHT = 'light'
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'

class Sensor(ABC):
    def __init__(self, sensor_id: str, type: SensorType, zone, field,min_value, max_value, value=None):
        self.sensor_id = sensor_id
        self.value = value
        self.type = type
        self.min_value = min_value
        self.max_value = max_value
        self.is_simulating = True
        self.zone = zone
        self.field = field

    def start_mqtt(self):
        self._setup_mqtt_client()
        self.thread.start()

    def _setup_mqtt_client(self):
        try:
            host, port = self._parse_mqtt_url(MQTT_BROKER_URL)
            self.client.connect(host, port)
            self.consumption_topic = CONSUMPTION_TOPIC.format(
                zone_id=self.zone.zone_id,
                field_id=self.field.field_id
            )
        except Exception as e:
            logger.error(f"Failed to setup MQTT client: {e}")
            raise

    @abstractmethod
    def simulate_value(self):
        pass

    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))

    def to_dict(self):
        return {
            'sensor_id': self.sensor_id,
            'type': self.type.value,
            'value': self.value,
            'min_value': self.min_value,
            'max_value': self.max_value
        }

class SoilMoistureSensor(Sensor):

    def simulate_value(self):
        if self.is_simulating:
            value = self.value + random.uniform(-2, 2)
            self.value = max(self.min_value, min(self.max_value, value))
        return self.value

class LightSensor(Sensor):
    def simulate_value(self):
        value = self.value + random.uniform(-50, 50)
        self.value = max(self.min_value, min(self.max_value, value))
        return self.value

class HumiditySensor(Sensor):
    def simulate_value(self):
        value = self.value + random.uniform(-5, 5)
        self.value = max(self.min_value, min(self.max_value, value))
        return self.value

class TemperatureSensor(Sensor):
    def simulate_value(self):
        value = self.value + random.uniform(-1, 1)
        self.value = max(self.min_value, min(self.max_value, value))
        return self.value

class SensorFactory:
    SENSOR_MAP = {
        SensorType.SOIL_MOISTURE.value: SoilMoistureSensor,
        SensorType.LIGHT.value: LightSensor,
        SensorType.HUMIDITY.value: HumiditySensor,
        SensorType.TEMPERATURE.value: TemperatureSensor
    }

    @staticmethod
    def create_sensor(**kwargs):
        sensor_type = kwargs.get('type', '')
        if sensor_type not in SensorFactory.SENSOR_MAP:
            raise ValueError(f"Invalid sensor type: {sensor_type}")
        return SensorFactory.SENSOR_MAP[sensor_type](**kwargs)