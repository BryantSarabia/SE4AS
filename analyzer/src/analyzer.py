import json
import logging
from time import sleep
from typing import Dict, Optional

import paho.mqtt.client as mqtt
from config import Config
from field import Field
from sensor import SensorFactory, SensorType
from src.weather import WeatherFetcher
from user_preferences import UserPreferences
from zone import Zone, ZoneService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Analyzer:
    def __init__(self, config: Config):
        self.config = config
        self.user_preferences_service = UserPreferences(config.BACKEND_URL)
        self._setup_mqtt_client()
        self.zone_service = ZoneService(config.BACKEND_URL)
        self.zones: Dict[str, Zone] = {}
        self.weather_fetcher = WeatherFetcher(config.WEATHER_API_KEY)
        self.moisture_threshold = self._get_moisture_threshold()

    def _setup_mqtt_client(self) -> None:
        try:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self._on_connect
            self.mqtt_client.on_message = self._on_message
            host, port = self._parse_mqtt_url(self.config.MQTT_BROKER_URL)
            self.mqtt_client.connect(host, port, self.config.MQTT_KEEPALIVE)
            self.mqtt_client.loop_start()
        except Exception as e:
            logger.error(f"Failed to setup MQTT client: {e}")
            raise

    @staticmethod
    def _parse_mqtt_url(url: str) -> tuple[str, int]:
        parts = url.split(":")
        return parts[0], int(parts[1]) if len(parts) > 1 else 1883

    def _on_connect(self, client, userdata, flags, rc: int) -> None:
        logger.info(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("zone/#")
        self._load_zones()

    def _load_zones(self) -> None:
        try:
            zones = self.zone_service.get_zones()
            for zone in zones:
                self._process_zone(zone)
        except Exception as e:
            logger.error(f"Failed to load zones: {e}")

    def _process_zone_data(self, zone: Zone) -> None:
        self.zones[zone['zone_id']] = zone

    def _create_field(self, field_data: dict) -> Field:
        field = Field(
            field_data['field_id'],
            field_data['latitude'],
            field_data['longitude']
        )
        for sensor_data in field_data['sensors']:
            self._add_sensor_to_field(field, sensor_data)
        return field

    def _add_sensor_to_field(self, field: Field, sensor_data: dict) -> None:
        sensor_type = SensorType(sensor_data['sensor_type'])
        sensor = SensorFactory.create_sensor(
            sensor_type,
            **sensor_data,
            latitude=field.latitude,
            longitude=field.longitude
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

    def analyze_data(self, zone_id: str, field_id: str) -> Optional[dict]:
        try:
            field = self.zones[zone_id].fields[field_id]
            soil_moisture_avg = field.get_average_sensor_value(SensorType.SOIL_MOISTURE)
            
            if soil_moisture_avg is None:
                return None

            rain_prediction = self._is_rain_predicted(field.latitude, field.longitude)
            self.moisture_threshold = self._get_moisture_threshold()

            return self._determine_irrigation_action(soil_moisture_avg, rain_prediction)
        except Exception as e:
            logger.error(f"Error analyzing data for zone {zone_id}, field {field_id}: {e}")
            return None

    def _determine_irrigation_action(
        self, 
        soil_moisture_avg: float, 
        rain_prediction: bool
    ) -> Optional[dict]:
        if soil_moisture_avg <= self.moisture_threshold and not rain_prediction:
            return {
                "action": "trigger_irrigation",
                "reason": "(Sml ≤ Smt) ⋀ ⌐Rp"
            }
        elif soil_moisture_avg > self.moisture_threshold or rain_prediction:
            return {
                "action": "stop_irrigation",
                "reason": "(Sml > Smt) ⋁ Rp"
            }
        return None

    def run(self) -> None:
        while True:
            try:
                self._analyze_all_fields()
                sleep(self.config.ANALYSIS_INTERVAL)
            except Exception as e:
                logger.error(f"Error in main analysis loop: {e}")
                sleep(self.config.ANALYSIS_INTERVAL)

    def _analyze_all_fields(self) -> None:
        for zone_id, zone in self.zones.items():
            for field_id in zone.fields:
                analysis_result = self.analyze_data(zone_id, field_id)
                if analysis_result:
                    self._publish_analysis_result(zone_id, field_id, analysis_result)

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