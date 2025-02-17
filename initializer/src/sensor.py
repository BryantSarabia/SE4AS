 
import random
from abc import ABC, abstractmethod
from enum import Enum


class SensorType(Enum):
    SOIL_MOISTURE = 'soil_moisture'
    LIGHT = 'light'
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'

class Sensor(ABC):
    def __init__(self, sensor_id: str, type: SensorType, value=None, min_value=None, max_value=None):
        self.sensor_id = sensor_id
        self.value = value
        self.type = type
        self.min_value = min_value
        self.max_value = max_value

    @abstractmethod
    def simulate_value(self):
        pass

    def set_value(self, value):
         self.value = max(self.min_value, min(self.max_value, value))

    def to_dict(self):
        return {
            'sensor_id': self.sensor_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'type': self.type.value,
            'value': self.value,
            'min_value': self.min_value,
            'max_value': self.max_value
        }

class SoilMoistureSensor(Sensor):

    def simulate_value(self):
        value = self.value + random.uniform(-5, 5)
        self.value = max(self.min_value, min(self.max_value, value))
        return self.value
    
    def to_dict(self):
        return {
            **super().to_dict(),
        }

class LightSensor(Sensor):

    def simulate_value(self):
        value = self.value + random.uniform(-50, 50)
        self.value = max(self.min_value, min(self.max_value, value))
        return self.value
    
    def to_dict(self):
        return {
            **super().to_dict(),
        }

class HumiditySensor(Sensor):

    def simulate_value(self):
        value = self.value + random.uniform(-5, 5)
        self.value = max(self.min_value, min(self.max_value, value))
        return self.value
    
    def to_dict(self):
        return {
            **super().to_dict(),
        }
    
class TemperatureSensor(Sensor):

    def simulate_value(self):
        value = self.value + random.uniform(-1, 1)
        self.value = max(self.min_value, min(self.max_value, value))
        return self.value
    
    def to_dict(self):
        return {
            **super().to_dict(),
        }

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