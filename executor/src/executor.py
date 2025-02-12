import json
import os
import time

from paho.mqtt import client as mqtt

MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mqtt://mosquitto')
PLANNER_OUTPUT_TOPIC_PREFIX = 'planner/'
IRRIGATION_COMMAND_TOPIC_PREFIX = 'irrigation/'

class Executor:
    def __init__(self, mqtt_broker_url):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(mqtt_broker_url, 1883, 60)
        self.mqtt_client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(f"{PLANNER_OUTPUT_TOPIC_PREFIX}#")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = json.loads(msg.payload.decode())
        action = payload['action']
        reason = payload['reason']

        parts = topic.split('/')
        zone_id = parts[1]
        field_id = parts[3]

        topic = f"{IRRIGATION_COMMAND_TOPIC_PREFIX}{zone_id}/field/{field_id}/command"
        client.publish(topic, action)
        print(f"Executed action for {zone_id}/{field_id}: {action}, Reason: {reason}")

if __name__ == "__main__":
    executor = Executor(MQTT_BROKER_URL)