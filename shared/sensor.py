import math
import random
from abc import ABC, abstractmethod
from enum import Enum


class SensorType(Enum):
    SOIL_MOISTURE = 'soil_moisture'
    LIGHT = 'light'
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'

class Sensor(ABC):
    def __init__(self, sensor_id: str, latitude: float, longitude: float, type: SensorType, value=None, min_value=None, max_value=None):
        self.sensor_id = sensor_id
        self.latitude = latitude
        self.longitude = longitude
        self.value = value
        self.type = type
        self.min_value = min_value
        self.max_value = max_value

    @abstractmethod
    def simulate_value(self):
        pass

class SoilMoistureSensor(Sensor):
    def simulate_value(self):
        value = self.value + random.uniform(-5, 5)
        self.value = math.max(self.min_value, math.min(self.max_value, value))
        return self.value

class LightSensor(Sensor):
    def simulate_value(self):
        value = self.value + random.uniform(-50, 50)
        self.value = math.max(self.min_value, math.min(self.max_value, value))
        return self.value

class HumiditySensor(Sensor):
    def simulate_value(self):
        value = self.value + random.uniform(-5, 5)
        self.value = math.max(self.min_value, math.min(self.max_value, value))
        return self.value
    
class TemperatureSensor(Sensor):
    def simulate_value(self):
        value = self.value + random.uniform(-1, 1)
        self.value = math.max(self.min_value, math.min(self.max_value, value))
        return self.value

class SensorFactory:
    SENSOR_MAP = {
        SensorType.SOIL_MOISTURE: SoilMoistureSensor,
        SensorType.LIGHT: LightSensor,
        SensorType.HUMIDITY: HumiditySensor,
        SensorType.TEMPERATURE: TemperatureSensor
    }
    @staticmethod
    def create_sensor(**kwargs):
        sensor_type = kwargs.get('type', '')
        if sensor_type not in SensorFactory.SENSOR_MAP:
            raise ValueError(f"Invalid sensor type: {sensor_type}")
        return SensorFactory.SENSOR_MAP[sensor_type](**kwargs)