import json
import logging
import os
import threading
from abc import ABC, abstractmethod
from enum import Enum
from time import sleep
from typing import Tuple

import paho.mqtt.client as mqtt

EXECUTOR = 'executor/zone/{zone_id}/field/{field_id}'
CONSUMPTION_TOPIC = 'zone/{zone_id}/field/{field_id}/actuator/{actuator_id}/{actuator_type}/consumption'
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mosquitto:1883')
SPEED_UP_SOIL_MOISTURE_BY = 2 * 60 # 2 hours

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ActuatorType(Enum):
    SPRINKLER = 'sprinkler'
    DRIP_IRRIGATION = 'drip_irrigation'

class ActionType(Enum):
    START_IRRIGATION = 'start_irrigation'
    STOP_IRRIGATION = 'stop_irrigation'

class Actuator(ABC):

    def __init__(self, actuator_id: str, type: ActionType, zone_id: str, field_id: str, consumption: float, measurement: str, max_value, min_value):
        self.actuator_id = actuator_id
        self.type = type
        self.value = None
        self.max_value = max_value
        self.min_value = min_value
        self.zone_id = zone_id
        self.field_id = field_id
        self.consumption = consumption
        self.measurement = measurement
        self.status = 'off'
        self._setup_mqtt_client()
        self._consumption_thread = None

    def calculate_power_percentage(self, water_need: float) -> float:
        """
        Calculate the percentage of power that the actuator should be operating at.
        
        :param water_need: The water need of the field in liters.
        :return: The percentage of power (0 to 100) that the actuator should be operating at.
        """
        try:
            required_runtime = water_need / self.consumption
            power_percentage = (required_runtime / 60) * 100
            power_percentage = max(self.min_value, min(self.max_value, power_percentage))
            return power_percentage
        except Exception as e:
            logger.error(f"Error calculating power percentage: {e}")
            return 0

    def _setup_mqtt_client(self) -> None:
        """Set up MQTT client with proper configuration."""
        try:
            self.topic = EXECUTOR.format(
                zone_id=self.zone_id,
                field_id=self.field_id
            )
            self.consumption_topic = CONSUMPTION_TOPIC.format(
                zone_id=self.zone_id,
                field_id=self.field_id,
                actuator_id=self.actuator_id,
                actuator_type=self.type
            )

            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self._on_connect
            self.mqtt_client.on_message = self._on_message
            
            host, port = self._parse_mqtt_url(MQTT_BROKER_URL)
            self.mqtt_client.connect(host, port, 60)
            self.mqtt_client.loop_start()
            
            logger.info(f"MQTT client setup completed for actuator {self.actuator_id}")
        except Exception as e:
            logger.error(f"Failed to setup MQTT client: {e}")
            raise

    def _parse_mqtt_url(self, url: str) -> Tuple[str, int]:
        parts = url.split(":")
        host = parts[0]
        port = int(parts[1])
        return host, port

    def _on_connect(self, client, userdata, flags, rc: int) -> None:
        if rc == 0:
            logger.info(f"Connected to MQTT broker for actuator {self.actuator_id}")
            client.subscribe(self.topic)
            logger.info(f"Subscribed to topic: {self.topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker with result code: {rc}")

    @abstractmethod
    def _on_message(self, client, userdata, msg):
        pass

    def start(self, value: float) -> None:
        if self.status == 'on':
            return
        try:
            self.value = max(self.min_value, min(self.max_value, value))
            self.status = 'on'
            self._start_consumption_thread()
            logger.info(f"Started actuator {self.actuator_id} with value {self.value}")
        except Exception as e:
            logger.error(f"Error starting actuator: {e}")
    
    def stop(self) -> None:
        if self.status == 'off':
            return
        try:
            self.value = None
            self.status = 'off'
            if self._consumption_thread and self._consumption_thread.is_alive():
                self._consumption_thread.join()
            payload = {
                'status': self.status,
                'value': 0,
                'measurement': self.measurement,
            }
            self.mqtt_client.publish(self.consumption_topic, json.dumps(payload))
            logger.info(f"Stopped actuator {self.actuator_id}")
        except Exception as e:
            logger.error(f"Error stopping actuator: {e}")
    
    def _start_consumption_thread(self) -> None:
        self._consumption_thread = threading.Thread(target=self._publish_consumption)
        self._consumption_thread.start()
    
    def _publish_consumption(self) -> None:
        try:
            while self.status == 'on':
                payload = {
                    'value': ( ((self.value / self.max_value) * self.consumption) / 60 ) * SPEED_UP_SOIL_MOISTURE_BY,
                    'measurement': self.measurement,
                    'status': self.status
                }
                self.mqtt_client.publish(self.consumption_topic, json.dumps(payload))
                sleep(1)
        except Exception as e:
            logger.error(f"Error publishing consumption: {e}")
    
class Sprinkler(Actuator):
    def _on_message(self, client, userdata, msg) -> None:
        try:
            payload = json.loads(msg.payload.decode())
            action = payload.get('command')
            
            if not action:
                logger.warning("Received message without action")
                return
                
            if action == ActionType.START_IRRIGATION.value:
                water_need = payload.get('water_need')
                if water_need is None:
                    logger.error("Missing water need for start_irrigation")
                    return
                power_percentage = self.calculate_power_percentage(float(water_need))
                self.start(power_percentage)
            elif action == ActionType.STOP_IRRIGATION.value:
                self.stop()
            else:
                logger.warning(f"Unknown action received: {action}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

class DripIrrigation(Actuator):
    def _on_message(self, client, userdata, msg) -> None:
        try:
            payload = json.loads(msg.payload.decode())
            action = payload.get('command')
            
            if not action:
                logger.warning("Received message without action")
                return
                
            if action == ActionType.START_IRRIGATION.value:
                water_need = payload.get('water_need')
                if water_need is None:
                    logger.error("Missing water need for start_irrigation")
                    return
                power_percentage = self.calculate_power_percentage(float(water_need))
                self.start(power_percentage)
            elif action == ActionType.STOP_IRRIGATION.value:
                self.stop()
            else:
                logger.warning(f"Unknown action received: {action}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

class ActuatorFactory:

    ACTUATOR_MAP = {
        ActuatorType.SPRINKLER.value: Sprinkler,
        ActuatorType.DRIP_IRRIGATION.value: DripIrrigation
    }

    @staticmethod
    def create_actuator(**kwargs):
        try:
            actuator_type = kwargs.get('type')
            if not actuator_type or actuator_type not in ActuatorFactory.ACTUATOR_MAP:
                raise ValueError(f"Invalid actuator type: {actuator_type}")
                
            actuator_class = ActuatorFactory.ACTUATOR_MAP[actuator_type]
            return actuator_class(**kwargs)
            
        except Exception as e:
            logger.error(f"Error creating actuator: {e}")
            raise