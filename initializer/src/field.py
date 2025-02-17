from .actuator import Actuator
from .sensor import Sensor, SensorType


class Field:

    def __init__(self, field_id: str, soil_moisture_threshold: float):
        self.field_id = field_id
        self.sensors: dict[str, dict[str, Sensor]]  = {}
        self.actuators: dict[str, dict[str, Actuator]] = {}
        self.soil_moisture_threshold = soil_moisture_threshold

    def to_dict(self):
        return {
            'field_id': self.field_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'sensors': [sensor.to_dict() for sensor_dict in self.sensors.values() for sensor in sensor_dict.values()],
            'actuators': [actuator.to_dict() for actuator_dict in self.actuators.values() for actuator in actuator_dict.values()] 
        }

    def add_sensor(self, sensor: Sensor):
        if sensor.type not in self.sensors:
            self.sensors[sensor.type] = {}
        self.sensors[sensor.type].update({sensor.sensor_id: sensor})
    
    def add_actuator(self, actuator: Actuator):
        if actuator.type not in self.actuators:
            self.actuators[actuator.type] = {}
        self.actuators[actuator.type].update({actuator.actuator_id: actuator})

    def get_average_sensor_value(self, sensor_type: SensorType):
        if sensor_type in self.sensors:
            sensors = self.sensors[sensor_type]
            values = [sensor.value for sensor in sensors if sensor.value is not None]
            return sum(values) / len(values) if values else None
        return None
    
    def get_sensor(self, sensor_id: str):
        for sensor_dict in self.sensors.values():
            if sensor_id in sensor_dict:
                return sensor_dict[sensor_id]
        return None
    
    def get_all_sensors(self):
        return [sensor for sensor_dict in self.sensors.values() for sensor in sensor_dict.values()]