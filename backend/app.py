import logging
import os

import pymongo
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration
APP_PORT = int(os.getenv('BACKEND_PORT', 5000))
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'se4as')
MONGO_COLLECTION_NAME = os.getenv('MONGO_ZONE_COLLECTION_NAME', 'zones')
PREFERENCES_COLLECTION_NAME = os.getenv('MONGO_PREFERENCES_COLLECTION_NAME', 'preferences')

# MongoDB Client
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
zones_collection = db[MONGO_COLLECTION_NAME]
preferences_collection = db[PREFERENCES_COLLECTION_NAME]

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Routes
@app.route('/zones', methods=['GET'])
def get_zones():
    try:
        zones = list(zones_collection.find({}, {'_id': 0}))
        return jsonify(zones)
    except Exception as e:
        logger.error(f"Error fetching zones: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/zones', methods=['POST'])
def create_zone():
    try:
        data = request.json
        zones_collection.insert_one(data)
        return jsonify(data), 201
    except Exception as e:
        logger.error(f"Error creating zone: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/zones/<zone_id>/fields/<field_id>', methods=['GET'])
def get_field(zone_id, field_id):
    try:
        zone = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0})
        if zone:
            field = zone['fields'].get(field_id)
            if field:
                return jsonify(field)
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching field: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/zones/<zone_id>/fields', methods=['POST'])
def create_field(zone_id):
    try:
        data = request.json
        field = {"field_id": data["field_id"], "sensors": data["sensors"], "actuators": data["actuators"]}
        zones_collection.update_one({'zone_id': zone_id}, {'$set': {f'fields.{field["field_id"]}': field}}, upsert=True)
        return jsonify(field), 201
    except Exception as e:
        logger.error(f"Error creating field: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/preferences', methods=['GET'])
def get_preferences():
    try:
        preferences = preferences_collection.find_one({}, {'_id': 0})
        if preferences:
            return jsonify(preferences)
        else:
            return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching preferences: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/preferences', methods=['POST'])
def create_preference():
    try:
        data = request.json
        preferences_collection.insert_one(data)
        return jsonify(data), 201
    except Exception as e:
        logger.error(f"Error creating preference: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/preferences', methods=['PUT'])
def update_preference():
    try:
        data = request.json
        preferences_collection.update_one({}, {'$set': data}, upsert=True)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error updating preference: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/preferences', methods=['DELETE'])
def delete_preference():
    try:
        preferences_collection.delete_one({})
        return jsonify({}), 204
    except Exception as e:
        logger.error(f"Error deleting preference: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=APP_PORT)