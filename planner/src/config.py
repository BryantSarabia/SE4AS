from dataclasses import dataclass


@dataclass
class Config:
    MQTT_BROKER_URL: str
    MQTT_KEEPALIVE: int = 60
    ANALYZER_TOPIC_PREFIX: str = 'analyzer'
    PLANNER_TOPIC_PREFIX: str = 'planner'