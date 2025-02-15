from dataclasses import dataclass


@dataclass
class Config:
    MQTT_BROKER_URL: str
    MQTT_KEEPALIVE: int = 60
    PLANNER_TOPIC_PREFIX: str = 'planner'
    EXECUTOR_TOPIC_PREFIX: str = 'executor'