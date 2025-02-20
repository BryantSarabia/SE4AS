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

class Planner:
    def __init__(self, config: Config):
        self.config = config
        self._setup_mqtt_client()

    def _setup_mqtt_client(self) -> None:
        try:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self._on_connect
            self.mqtt_client.on_message = self._on_message
            
            host, port = self._parse_mqtt_url(self.config.MQTT_BROKER_URL)
            self.mqtt_client.connect(host, port, self.config.MQTT_KEEPALIVE)
            
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
            topic = f"{self.config.ANALYZER_TOPIC_PREFIX}/#"
            client.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker with result code: {rc}")

    def _on_message(self, client, userdata, msg) -> None:
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            zone_id, field_id = self._parse_topic(topic)
            if not zone_id or not field_id:
                logger.error(f"Invalid topic format: {topic}")
                return

            plan = self._generate_plan(payload)
            if plan:
                self._publish_plan(zone_id, field_id, plan)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload received: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _parse_topic(self, topic: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            parts = topic.split('/')
            return parts[2], parts[4]
        except IndexError:
            return None, None

    def _generate_plan(self, payload: Dict) -> Optional[Dict]:
        try:
            action = payload.get('action')
            reason = payload.get('reason')

            if not action or not reason:
                logger.error("Missing action or reason in payload")
                return None

            if action == "trigger_irrigation":
                return {"action": "start_irrigation", "reason": reason, "value": 100}
            elif action == "stop_irrigation":
                return {"action": "stop_irrigation", "reason": reason}
            else:
                logger.warning(f"Unknown action received: {action}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating plan: {e}")
            return None

    def _publish_plan(self, zone_id: str, field_id: str, plan: Dict) -> None:
        try:
            topic = f"{self.config.PLANNER_TOPIC_PREFIX}/zone/{zone_id}/field/{field_id}"
            self.mqtt_client.publish(topic, json.dumps(plan))
            logger.info(f"Published plan for {zone_id}/{field_id}: {plan}")
        except Exception as e:
            logger.error(f"Error publishing plan: {e}")

    def run(self) -> None:
        try:
            logger.info("Starting Planner service...")
            self.mqtt_client.loop_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down Planner service...")
            self.mqtt_client.disconnect()
        except Exception as e:
            logger.error(f"Error in Planner service: {e}")
            self.mqtt_client.disconnect()