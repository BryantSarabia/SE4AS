import requests
from field import Field


class Zone:
    def __init__(self, zone_id: str):
        self.zone_id = zone_id
        self.fields: dict[str, Field] = {}

    def add_field(self, field):
        self.fields[field.field_id] = field

class ZoneService:     
  
    def __init__(self, backend_url: str):
        self.backend_url = backend_url

    def get_zones(self) -> list[Zone]:
        response = requests.get(f"{self.backend_url}/zones")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch zones: {response.status_code}")
            return []
        
    def add_zone(self, zone):
        response = requests.post(f"{self.backend_url}/zones", json=zone)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Failed to create zone: {response.status_code}")
            return None
        
    def add_field(self, zone_id, field):
        response = requests.post(f"{self.backend_url}/zones/{zone_id}/fields", json=field)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Failed to create field: {response.status_code}")
            return None