import requests


class UserPreferences:
    def __init__(self, backend_url: str):
        self.backend_url = backend_url

    def get(self):
        response = requests.get(f"{self.backend_url}/preferences")
        if response.status_code == 200:
            self.preferences = response.json()
        else:
            print(f"Failed to fetch preferences: {response.status_code}")
            return None

    def create(self, preferences):
        response = requests.post(f"{self.backend_url}/preferences", json=preferences)
        if response.status_code == 201:
            self.preferences = preferences
        else:
            print(f"Failed to create preferences: {response.status_code}")

    def update(self, preferences):
        response = requests.put(f"{self.backend_url}/preferences", json=preferences)
        if response.status_code == 200:
            self.preferences = preferences
        else:
            print(f"Failed to update preferences: {response.status_code}")

    def delete(self):
        response = requests.delete(f"{self.backend_url}/preferences")
        if response.status_code == 204:
            self.preferences = {}
        else:
            print(f"Failed to delete preferences: {response.status_code}")