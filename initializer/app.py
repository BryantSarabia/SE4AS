import json
import logging
import os
import sys

import requests
from src.zone import ZoneService

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:80')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize():
    zone_service = ZoneService(BACKEND_URL)
    zones = zone_service.get_zones()
    logger.info(zones)
    if zones:
        logger.info("MongoDB already initialized.")
        sys.exit(0)
        return

    with open('zones.json') as f:
        zones_data = json.load(f)
        for zone_data in zones_data:
          requests.post(f"{BACKEND_URL}/zones", json=zone_data)
    logger.info("MongoDB initialized with data.")
    sys.exit(0)


if __name__ == "__main__":
    initialize()