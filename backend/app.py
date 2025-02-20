import logging
import os

import pymongo
from bson import ObjectId
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


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

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

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
        result = zones_collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return jsonify(data), 201
    except Exception as e:
        logger.error(f"Error creating zone: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route('/zones/<zone_id>/fields/sensors', methods=['GET'])
def get_all_sensors(zone_id):
    try:
        zone = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0})
        if zone:
            sensors = []
            for field in zone['fields']:
                if(field['sensors']):
                    sensors.extend(field['sensors'])
            return jsonify(sensors)
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching sensors: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route('/zones/<zone_id>/fields/sensors/count', methods=['GET'])
def get_all_sensors_count(zone_id):
    try:
        zone = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0})
        if zone:
            sensors = []
            for field in zone['fields']:
                if(field['sensors']):
                    sensors.extend(field['sensors'])
            return jsonify(len(sensors))
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching sensors: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route('/zones/<zone_id>/fields/actuators/count', methods=['GET'])
def get_all_actuators_count(zone_id):
    try:
        zone = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0})
        if zone:
            actuators = []
            for field in zone['fields']:
                if(field['actuators']):
                    actuators.extend(field['actuators'])
            return jsonify(len(actuators))
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching actuators: {e}")
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
    
@app.route('/zones/<zone_id>/fields/<field_id>/sensors', methods=['GET'])
def get_sensors(zone_id, field_id):
    try:
        zone = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0})
        if zone:
            field = zone['fields'].get(field_id)
            if field:
                return jsonify(field['sensors'])
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching sensors: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route('/zones/<zone_id>/fields/<field_id>/actuators', methods=['GET'])
def get_actuators(zone_id, field_id):
    try:
        zone = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0})
        if zone:
            field = zone['fields'].get(field_id)
            if field:
                return jsonify(field['actuators'])
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching actuators: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/zones/<zone_id>/fields', methods=['GET'])
def get_fields(zone_id):
    try:
        zone = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0})
        if zone:
            return jsonify(zone['fields'])
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching fields: {e}")
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
    
@app.route('/zones/<zone_id>/fields/<field_id>/soil_moisture_threshold', methods=['GET'])
def get_soil_moisture_threshold(zone_id, field_id):
    try:
        soil_moisture_threshold = zones_collection.find_one({'zone_id': zone_id, 'fields.field_id': field_id}, {'_id': 0, 'fields.$': 1})
        if soil_moisture_threshold:
            return jsonify(soil_moisture_threshold['fields'][0].get('soil_moisture_threshold', {}))
        return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching soil moisture threshold: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
#zones/coppito/fields/coppito_pomodori/soil_moisture_threshold
@app.route('/zones/<zone_id>/fields/<field_id>/soil_moisture_threshold', methods=['PUT'])
def create_soil_moisture_threshold(zone_id, field_id):
    try:
        data = request.json
        soil_moisture_threshold = data.get('soil_moisture_threshold', None)
        if soil_moisture_threshold is None:
            return jsonify({"error": "soil_moisture_threshold is required"}), 400

        zones_collection.update_one(
            {'zone_id': zone_id, 'fields.field_id': field_id},
            {'$set': {'fields.$.soil_moisture_threshold': soil_moisture_threshold}}
        )
        return jsonify(data), 201
    except Exception as e:
        logger.error(f"Error updating soil moisture threshold: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/zones/<zone_id>/preferences', methods=['GET'])
def get_preferences(zone_id):
    try:
        preferences = zones_collection.find_one({'zone_id': zone_id}, {'_id': 0, 'preferences': 1})
        if preferences:
            return jsonify(preferences)
        else:
            return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error fetching preferences: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/zones/<zone_id>/preferences', methods=['POST'])
def create_preference(zone_id):
    try:
        data = request.json
        zones_collection.update_one({'zone_id': zone_id}, {'$set': {'preferences': data}}, upsert=True)
        return jsonify(data), 201
    except Exception as e:
        logger.error(f"Error creating preference: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/zones/<zone_id>/preferences', methods=['PUT'])
def update_preference(zone_id):
    try:
        data = request.json
        zones_collection.update_one({'zone_id': zone_id}, {'$set': {'preferences': data}}, upsert=True)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error updating preference: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)