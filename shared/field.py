from actuator import Actuator
from sensor import Sensor, SensorType


class Field:

    def __init__(self, field_id: str, latitude: float, longitude: float):
        self.field_id = field_id
        self.latitude = latitude
        self.longitude = longitude
        self.sensors: dict[str, dict[str, Sensor]]  = {}
        self.actuators: dict[str, dict[str, Actuator]] = {}

    def to_dict(self):
        return {
            'field_id': self.field_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'sensors': [sensor.to_dict() for sensor_dict in self.sensors.values() for sensor in sensor_dict.values()],
            'actuators': [actuator.to_dict() for actuator_dict in self.actuators.values() for actuator in actuator_dict.values()] 
        }

    def add_sensor(self, sensor: Sensor):
        if sensor.sensor_type not in self.sensors:
            self.sensors[sensor.sensor_type] = []
        self.sensors[sensor.sensor_type].update({sensor.sensor_id: sensor})

    

    def get_average_sensor_value(self, sensor_type: SensorType):
        if sensor_type in self.sensors:
            sensors = self.sensors[sensor_type]
            values = [sensor.value for sensor in sensors if sensor.value is not None]
            return sum(values) / len(values) if values else None
        return None