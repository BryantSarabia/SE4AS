import json

from paho.mqtt import client as mqtt

ANALYZER_OUTPUT_TOPIC_PREFIX = 'analyzer/'
PLANNER_OUTPUT_TOPIC_PREFIX = 'planner/'

class Planner:
    def __init__(self, mqtt_broker_url):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        broker_mqtt_port = mqtt_broker_url.split(":")[:-1]
        self.mqtt_client.connect(mqtt_broker_url, broker_mqtt_port, 60)
        self.mqtt_client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(f"{ANALYZER_OUTPUT_TOPIC_PREFIX}#")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode())
        action = payload['action']
        reason = payload['reason']

        parts = topic.split('/')
        zone_id = parts[1]
        field_id = parts[3]

        if action == "trigger_irrigation":
            plan = {"action": "start_irrigation", "reason": reason}
        elif action == "stop_irrigation":
            plan = {"action": "stop_irrigation", "reason": reason}

        topic = f"{PLANNER_OUTPUT_TOPIC_PREFIX}{zone_id}/field/{field_id}/output"
        client.publish(topic, json.dumps(plan))
        print(f"Generated plan for {zone_id}/{field_id}: {plan}")

