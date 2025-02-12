import json
import os
from time import sleep

import paho.mqtt.client as mqtt
from field import Field
from sensor import SensorFactory, SensorType
from src.weather import WeatherFetcher
from user_preferences import UserPreferences
from zone import Zone, ZoneService

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', "")
ANALYZER_OUTPUT_TOPIC_PREFIX = 'analyzer/'

class Analyzer:
    def __init__(self, mqtt_broker_url: str, backend_url: str, UserPreferences: UserPreferences):
        self.user_preferences_service = UserPreferences(backend_url)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        mqtt_broker_port = mqtt_broker_url.split(":")[1:]
        self.mqtt_client.connect(mqtt_broker_url, mqtt_broker_port, 60)
        self.mqtt_client.loop_start()
        self.backend_url = backend_url
        self.zone_service = ZoneService(backend_url)
        self.zones = {}
        self.weather_fetcher = WeatherFetcher(WEATHER_API_KEY)
        self.moisture_threshold = self.get_moisture_threshold()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(f"zone/#")
        self.load_zones()

    def load_zones(self):
        zones_data = self.zone_service.get_zones()
        for zone_data in zones_data:
            zone = Zone(zone_data['zone_id'])
            for field_data in zone_data['fields']:
                field = Field(field_data['field_id'], field_data['latitude'], field_data['longitude'])
                for sensor_data in field_data['sensors']:
                    sensor_type = SensorType(sensor_data['sensor_type'])
                    sensor = SensorFactory.create_sensor(sensor_type, **sensor_data, **field)
                    field.add_sensor(sensor)
                zone.add_field(field)
            self.zones[zone_data['zone_id']] = zone

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode())

        if topic.startswith("zone/"):
            # zone/zone_id/field/field_id/sensor/sensor_id/sensor_type/latitude/longitude 
            _, zone_id, _, field_id, _, sensor_id, sensor_type, latitude, longitude = topic.split('/')
            value = payload['value']

            if zone_id not in self.zones:
                created_zone = self.zone_service.create_zone({"zone_id": zone_id})
                if not created_zone:
                    return
                self.zones[zone_id] = Zone(zone_id)

            if field_id not in self.zones[zone_id].fields:
                created_field = self.zone_service.create_field(zone_id, {"field_id": field_id, "latitude": latitude, "longitude": longitude})
                if created_field:
                  self.zones[zone_id].fields[field_id] = Field(field_id, latitude, longitude)
                else:
                    print(f"Failed to create field {field_id} for zone {zone_id}")

            if sensor_id not in self.zones[zone_id].fields[field_id].sensors[sensor_type]:
              sensor = SensorFactory.create_sensor(sensor_id, latitude, longitude, type=sensor_type)
              sensor.value = value
            else: 
              sensor = self.zones[zone_id].fields[field_id].sensors[sensor_type][sensor_id]
              sensor.value = value

    def analyze_data(self, zone_id, field_id):
        field = self.zones[zone_id].fields[field_id]
        soil_moisture_avg = field.get_average_sensor_value(SensorType.SOIL_MOISTURE)
        latitude, longitude = (field.latitude, field.longitude)
        if soil_moisture_avg is None:
            return None
        rain_prediction = self.is_rain_predicted(latitude, longitude)
        self.moisture_threshold = self.get_moisture_threshold()
        if soil_moisture_avg <= self.moisture_threshold and not rain_prediction:
            return {"action": "trigger_irrigation", "reason": "(Sml ≤ Smt) ⋀ ⌐Rp"}
        elif soil_moisture_avg > self.moisture_threshold or rain_prediction:
            return {"action": "stop_irrigation", "reason": "(Sml > Smt) ⋁ Rp"}

        return None
    
    def is_rain_predicted(self, latitude, longitude):
        weather_data = self.weather_fetcher.get_weather(latitude, longitude)
        if weather_data is None:
            return False
        return any(forecast['weather'][0]['main'] == 'Rain' for forecast in weather_data)

    def run(self):
        while True:
            for zone_id, zone in self.zones.items():
                for field_id in zone.fields:
                    analysis_result = self.analyze_data(zone_id, field_id)
                    if analysis_result:
                        topic = f"{ANALYZER_OUTPUT_TOPIC_PREFIX}{zone_id}/field/{field_id}"
                        self.mqtt_client.publish(topic, json.dumps(analysis_result))
                        print(f"Analysis result for {zone_id}/{field_id}: {analysis_result}")
            sleep(60)  # Analyze every minute
    
    def get_moisture_threshold(self):
        user_preferences = self.user_preferences_service.get()
        return user_preferences['moisture_threshold']