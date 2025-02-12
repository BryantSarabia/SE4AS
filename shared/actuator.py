import json
import math
import os
from abc import ABC, abstractmethod
from enum import Enum
from time import sleep

import paho.mqtt.client as mqtt

ACTION_TOPIC = 'zone/{zone_id}/field/{field_id}/action/+'
CONSUMPTION_TOPIC = 'zone/{zone_id}/field/{field_id}/actuator/{actuator_id}/consumption'
MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL', 'mqtt://mosquitto:1883')

class ActionType(Enum):
    START_IRRIGATION = 'start_irrigation'
    STOP_IRRIGATION = 'stop_irrigation'

class Actuator(ABC):

    def __init__(self, actuator_id: str, type: ActionType, zone_id: str, field_id: str, consumption: float, measurement: str):
        self.actuator_id = actuator_id
        self.type = type
        self.value = None
        self.max_value = None
        self.min_value = None
        self.zone_id = zone_id
        self.field_id = field_id
        self.consumption = consumption
        self.status = 'off'
        self.topic = ACTION_TOPIC.format(zone_id=zone_id, field_id=field_id)
        self.consumption_topic = CONSUMPTION_TOPIC.format(zone_id=zone_id, field_id=field_id, actuator_id=actuator_id)
        mqtt_broker_port = MQTT_BROKER_URL.split(":")[1:]
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER_URL, mqtt_broker_port, 60)
        self.mqtt_client.loop_start()

    @abstractmethod
    def on_message(self, client, userdata, msg):
        pass

    def start(self, value):
        self.value = math.max(self.min_value, math.min(self.max_value, value))
        self.status = 'on'
        self.publishConsumption()
    
    def stop(self):
        self.value = None
        self.status = 'off'
    
    def on_connect(self, client, userdata):
        client.subscribe(self.topic)
    
    def publishConsumption(self):
        while self.status == 'on':
          self.mqtt_client.publish(self.consumption_topic, json.dumps({'value': self.consumption, "measurement"}))
          sleep(1)
    
class Sprinkler(Actuator):
    
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        action = topic.split('/')[:-1]
        if action == ActionType.START_IRRIGATION:
            self.start(payload["value"])
        elif action == ActionType.STOP_IRRIGATION:
            self.stop()

    
class DripIrrigation(Actuator):

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        action = topic.split('/')[:-1]
        if action == ActionType.START_IRRIGATION:
            self.start(payload["value"])
        elif action == ActionType.STOP_IRRIGATION:
            self.stop()

class ActuatorFactory:
    ACTUATOR_MAP = {
        ActionType.START_IRRIGATION: Sprinkler,
        ActionType.STOP_IRRIGATION: DripIrrigation
    }
    @staticmethod
    def create_actuator(**kwargs):
        actuator_type = kwargs.get('type', '')
        if actuator_type not in ActuatorFactory.ACTUATOR_MAP:
            raise ValueError(f"Invalid actuator type: {actuator_type}")
        return ActuatorFactory.ACTUATOR_MAP[actuator_type](**kwargs)