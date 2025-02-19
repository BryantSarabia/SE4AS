from dataclasses import dataclass


@dataclass
class Config:
    MQTT_BROKER_URL: str
    BACKEND_URL: str
    WEATHER_API_KEY: str
    ANALYZER_OUTPUT_TOPIC_PREFIX: str = 'analyzer'
    MQTT_KEEPALIVE: int = 60
    NEXT_HOURS: int = 1