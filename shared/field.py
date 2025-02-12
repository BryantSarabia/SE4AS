from sensor import Sensor, SensorType


class Field:
    def __init__(self, field_id: str, latitude: float, longitude: float):
        self.field_id = field_id
        self.latitude = latitude
        self.longitude = longitude
        self.sensors: dict[SensorType, dict[str, Sensor]]  = {}

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