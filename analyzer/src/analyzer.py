import json
import logging
from time import sleep
from typing import Dict, Optional, Tuple

import paho.mqtt.client as mqtt

from .config import Config
from .field import Field
from .sensor import SensorFactory, SensorType
from .weather import WeatherFetcher
from .zone import Zone, ZoneService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Analyzer:
    def __init__(self, config: Config):
        self.config = config
        self.zone_service = ZoneService(config.BACKEND_URL)
        self.zones: Dict[str, Zone] = {}
        self.weather_fetcher = WeatherFetcher(config.WEATHER_API_KEY)
        self._load_zones()

    def run(self) -> None:
        self._setup_mqtt_client()

    def _setup_mqtt_client(self) -> None:
        try:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self._on_connect
            self.mqtt_client.on_message = self._on_message
            host, port = self._parse_mqtt_url(self.config.MQTT_BROKER_URL)
            self.mqtt_client.connect(host, port, self.config.MQTT_KEEPALIVE)
            self.mqtt_client.loop_forever()
        except Exception as e:
            logger.error(f"Failed to setup MQTT client: {e}")
            raise

    def _parse_mqtt_url(self, url: str) -> Tuple[str, int]:
        parts = url.split(":")
        host = parts[0]
        port = int(parts[1])
        return host, port

    def _on_connect(self, client, userdata, flags, rc: int) -> None:
        logger.info(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("zone/+/field/+/sensor/+/+")

    def _load_zones(self) -> None:
        try:
            zones = self.zone_service.get_zones()
            for zone in zones:
                self._process_zone(zone)
        except Exception as e:
            logger.error(f"Failed to load zones: {e}")

    def _process_zone(self, zone: Zone) -> None:
        self.zones[zone.zone_id] = zone

    def _create_field(self, field_data: dict) -> Field:
        field = Field(
            field_data['field_id']
        )
        for sensor_data in field_data['sensors']:
            self._add_sensor_to_field(field, sensor_data)
        return field

    def _add_sensor_to_field(self, field: Field, sensor_data: dict) -> None:
        sensor_type = SensorType(sensor_data['sensor_type'])
        sensor = SensorFactory.create_sensor(
            sensor_type,
            **sensor_data
        )
        field.add_sensor(sensor)

    def _on_message(self, client, userdata, msg) -> None:
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            self._process_message(topic, payload)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON payload received: {msg.payload}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _process_message(self, topic: str, payload: dict) -> None:
        parts = topic.split("/")
        zone_id = parts[1]
        field_id = parts[3]
        sensor_id = parts[5]
        field = self.zones[zone_id].get_field(field_id)
        if not field:
            logger.error(f"Field {field_id} not found in zone {zone_id}")
            return
        sensor = field.get_sensor(sensor_id)
        if not sensor:
            logger.error(f"Sensor {sensor_id} not found in field {field_id}")
            return
        logger.info(f"Received data for zone {zone_id}, field {field_id}, sensor {sensor_id}: {payload}")
        sensor.set_value(payload['value'])
        analysis_result = self.analyze_data(zone_id, field_id)
        if analysis_result:
            self._publish_analysis_result(zone_id, field_id, analysis_result)

    def analyze_data(self, zone_id: str, field_id: str) -> Optional[dict]:
        try:
            zone = self.zones[zone_id]
            field = zone.get_field(field_id)
            soil_moisture_threshold_avg = field.get_average_sensor_value(SensorType.SOIL_MOISTURE.value)
            
            if soil_moisture_threshold_avg is None:
                return None

            rain_prediction = self._is_rain_predicted(zone.latitude, zone.longitude)
            soil_moisture_threshold = field.soil_moisture_threshold

            return self._determine_irrigation_action(soil_moisture_threshold, soil_moisture_threshold_avg, rain_prediction)
        except Exception as e:
            logger.error(f"Error analyzing data for zone {zone_id}, field {field_id}: {e}")
            return None
    
    def _is_rain_predicted(self, lat: float, lon: float) -> bool:
        weather_data = self.weather_fetcher.get_weather(lat, lon)
        if not weather_data:
            return False
        try:
            offset = min(self.config.NEXT_HOURS, len(weather_data['list']) - 1)
            return 'rain' in weather_data['list'][offset]['weather'][0]['description'].lower()
        except Exception as e:
            logger.error(f"Error checking rain prediction: {e}")
            return False

    def _determine_irrigation_action(
        self, 
        soil_moisture_threshold: float,
        soil_moisture_threshold_avg: float, 
        rain_prediction: bool
    ) -> Optional[dict]:
        logger.info(f"Analyzing irrigation action: Smt: {soil_moisture_threshold}, Sml: {soil_moisture_threshold_avg}, Rp: {rain_prediction}")
        try:
            if soil_moisture_threshold_avg <= soil_moisture_threshold and not rain_prediction:
                return {
                    "action": "trigger_irrigation",
                    "reason": "(Sml ≤ Smt) ⋀ ⌐Rp"
                }
            elif soil_moisture_threshold_avg > soil_moisture_threshold or rain_prediction:
                return {
                    "action": "stop_irrigation",
                    "reason": "(Sml > Smt) ⋁ Rp"
                }
            return None
        except Exception as e:
            logger.info(f"Error determining irrigation action {e}")

    def _publish_analysis_result(
        self,
        zone_id: str,
        field_id: str,
        analysis_result: dict
    ) -> None:
        topic = f"{self.config.ANALYZER_OUTPUT_TOPIC_PREFIX}/zone/{zone_id}/field/{field_id}"
        try:
            self.mqtt_client.publish(topic, json.dumps(analysis_result))
            logger.info(f"Analysis result for {zone_id}/{field_id}: {analysis_result}")
        except Exception as e:
            logger.error(f"Failed to publish analysis result: {e}")