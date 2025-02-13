import logging
from typing import Dict, List, Optional

import requests
from field import Field
from requests.exceptions import RequestException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Zone:
    def __init__(self, zone_id: str):
        self.zone_id = zone_id
        self.fields: Dict[str, Field] = {}

    def add_field(self, field: Field) -> None:
        self.fields[field.field_id] = field
        logger.info(f"Added field {field.field_id} to zone {self.zone_id}")

    def to_dict(self) -> dict:
        return {
            "zone_id": self.zone_id,
            "fields": [field.to_dict() for field in self.fields.values()]
        }

class ZoneService:     
    def __init__(self, backend_url: str):
        self.backend_url = backend_url.rstrip('/')
        logger.info(f"Initialized ZoneService with backend URL: {backend_url}")

    def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> Optional[dict]:
        try:
            url = f"{self.backend_url}/{endpoint.lstrip('/')}"
            response = requests.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}, Status code: {e.response.status_code}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error connecting to backend: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    def get_zones(self) -> List[Zone]:
        try:
            data = self._make_request('GET', 'zones')
            if not data:
                return []

            zones = []
            for zone_data in data:
                zone = Zone(zone_data['zone_id'])
                for field_data in zone_data.get('fields', []):
                    field = Field(
                        field_data['field_id'],
                        field_data['latitude'],
                        field_data['longitude']
                    )
                    zone.add_field(field)
                zones.append(zone)
            return zones
        except Exception as e:
            logger.error(f"Error processing zones data: {e}")
            return []

    def add_zone(self, zone: Zone) -> Optional[dict]:
        try:
            zone_data = zone.to_dict()
            return self._make_request('POST', 'zones', zone_data)
        except Exception as e:
            logger.error(f"Error adding zone: {e}")
            return None

    def add_field(self, zone_id: str, field: Field) -> Optional[dict]:
        try:
            field_data = field.to_dict()
            return self._make_request('POST', f'zones/{zone_id}/fields', field_data)
        except Exception as e:
            logger.error(f"Error adding field: {e}")
            return None

    def get_zone(self, zone_id: str) -> Optional[Zone]:
        try:
            data = self._make_request('GET', f'zones/{zone_id}')
            if not data:
                return None

            zone = Zone(data['zone_id'])
            for field_data in data.get('fields', []):
                field = Field(
                    field_data['field_id'],
                    field_data['latitude'],
                    field_data['longitude']
                )
                zone.add_field(field)
            return zone
        except Exception as e:
            logger.error(f"Error fetching zone {zone_id}: {e}")
            return None