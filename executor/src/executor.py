import json
import logging
from typing import Dict, Optional, Tuple

from paho.mqtt import client as mqtt

from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Executor:
    def __init__(self, config: Config):
        self.config = config
        self._setup_mqtt_client()

    def _setup_mqtt_client(self) -> None:
        try:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self._on_connect
            self.mqtt_client.on_message = self._on_message
            host, port = self._parse_mqtt_url(self.config.MQTT_BROKER_URL)
            self.mqtt_client.connect(
                host,
                port,
                self.config.MQTT_KEEPALIVE
            )
            
            logger.info("MQTT client setup completed")
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
            logger.info("Connected to MQTT broker successfully")
            topic = f"{self.config.PLANNER_TOPIC_PREFIX}/#"
            client.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker with result code: {rc}")

    def _on_message(self, client, userdata, msg) -> None:
        try:
            topic = msg.topic
            try:
                payload = self._parse_payload(msg.payload)
            except Exception as e:
                logger.error(f"Error parsing payload: {e}")
                return
            try:
                zone_id, field_id = self._parse_topic(topic)
            except Exception as e:
                logger.error(f"Error parsing topic: {e}")
                return
            if not zone_id or not field_id:
                logger.error(f"Invalid topic format: {topic}")
                return

            self._execute_action(client, zone_id, field_id, payload)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _parse_payload(self, payload: bytes) -> Dict:
        try:
            data = json.loads(payload.decode())
            if not isinstance(data, dict):
                raise ValueError("Payload must be a JSON object")
            
            action = data.get('action')
            reason = data.get('reason')
            
            if not action or not reason:
                raise ValueError("Missing required fields in payload")
                
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
            raise
        except ValueError as e:
            logger.error(str(e))
            raise

    def _parse_topic(self, topic: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            parts = topic.split('/')
            return parts[2], parts[4]
        except IndexError:
            return None, None

    def _execute_action(self, client: mqtt.Client, zone_id: str, field_id: str, payload: Dict) -> None:
        try:
            action = payload['action']
            value = payload['value']
            reason = payload['reason']
            
            topic = f"{self.config.EXECUTOR_TOPIC_PREFIX}/zone/{zone_id}/field/{field_id}"
            client.publish(topic, json.dumps({"command": action, "value": value}))
            
            logger.info(
                f"Executed action for {zone_id}/{field_id}: {action}, Reason: {reason}"
            )
        except Exception as e:
            logger.error(f"Error executing action: {e}")

    def run(self) -> None:
        try:
            logger.info("Starting Executor service...")
            self.mqtt_client.loop_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down Executor service...")
            self.mqtt_client.disconnect()
        except Exception as e:
            logger.error(f"Error in Executor service: {e}")
            self.mqtt_client.disconnect()