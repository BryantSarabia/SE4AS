import os

import pymongo

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'se4as')
MONGO_COLLECTION_NAME = os.getenv('MONGO_ZONE_COLLECTION_NAME', 'zones')

def initialize():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]

    zones_data = [
        {
            'zone_id': 'zone1',
            'fields': [
                {
                    'field_id': 'field1',
                    'latitude': 51.5074,
                    'longitude': -0.1278,
                    'sensors': [
                        {'sensor_id': 'sensor1', 'sensor_type': 'soil_moisture'},
                        {'sensor_id': 'sensor2', 'sensor_type': 'light'},
                        {'sensor_id': 'sensor3', 'sensor_type': 'humidity'}
                    ]
                },
                {
                    'field_id': 'field2',
                    'latitude': 40.7128,
                    'longitude': -74.0060,
                    'sensors': [
                        {'sensor_id': 'sensor4', 'sensor_type': 'soil_moisture'},
                        {'sensor_id': 'sensor5', 'sensor_type': 'light'},
                        {'sensor_id': 'sensor6', 'sensor_type': 'humidity'}
                    ]
                }
            ]
        },
        {
            'zone_id': 'zone2',
            'fields': [
                {
                    'field_id': 'field3',
                    'latitude': 34.0522,
                    'longitude': -118.2437,
                    'sensors': [
                        {'sensor_id': 'sensor7', 'sensor_type': 'soil_moisture'},
                        {'sensor_id': 'sensor8', 'sensor_type': 'light'},
                        {'sensor_id': 'sensor9', 'sensor_type': 'humidity'}
                    ]
                }
            ]
        }
    ]

    for zone_data in zones_data:
        collection.insert_one(zone_data)

    print("MongoDB initialized with data.")

if __name__ == "__main__":
    initialize_mongodb()