import logging
from typing import Any, Dict, Optional

import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UserPreferences:
    def __init__(self, backend_url: str):
        self.backend_url = backend_url.rstrip('/')
        self.preferences: Optional[Dict[str, Any]] = None

    def get(self) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(f"{self.backend_url}/preferences")
            response.raise_for_status()
            self.preferences = response.json()
            return self.preferences
        except HTTPError as e:
            logger.error(f"HTTP error occurred: {e}, Status code: {e.response.status_code}")
        except ConnectionError as e:
            logger.error(f"Error connecting to backend: {e}")
        except RequestException as e:
            logger.error(f"Error making request: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return None

    def create(self, preferences: Dict[str, Any]) -> bool:
        try:
            response = requests.post(f"{self.backend_url}/preferences", json=preferences)
            response.raise_for_status()
            if response.status_code == 201:
                self.preferences = preferences
                return True
        except HTTPError as e:
            logger.error(f"HTTP error occurred: {e}, Status code: {e.response.status_code}")
        except ConnectionError as e:
            logger.error(f"Error connecting to backend: {e}")
        except RequestException as e:
            logger.error(f"Error making request: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return False

    def update(self, preferences: Dict[str, Any]) -> bool:
        try:
            response = requests.put(f"{self.backend_url}/preferences", json=preferences)
            response.raise_for_status()
            if response.status_code == 200:
                self.preferences = preferences
                return True
        except HTTPError as e:
            logger.error(f"HTTP error occurred: {e}, Status code: {e.response.status_code}")
        except ConnectionError as e:
            logger.error(f"Error connecting to backend: {e}")
        except RequestException as e:
            logger.error(f"Error making request: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return False

    def delete(self) -> bool:
        try:
            response = requests.delete(f"{self.backend_url}/preferences")
            response.raise_for_status()
            if response.status_code == 204:
                self.preferences = {}
                return True
        except HTTPError as e:
            logger.error(f"HTTP error occurred: {e}, Status code: {e.response.status_code}")
        except ConnectionError as e:
            logger.error(f"Error connecting to backend: {e}")
        except RequestException as e:
            logger.error(f"Error making request: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return False