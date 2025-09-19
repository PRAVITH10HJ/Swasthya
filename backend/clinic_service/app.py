from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import sqlite3
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- CONFIGURATION ---
DATABASE_PATH = 'health_services.db'

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@app.route('/clinics', methods=['GET'])
def get_clinics():
    try:
        user_lat = float(request.args.get('lat'))
        user_lon = float(request.args.get('lon'))
        radius_km = float(request.args.get('radius', 10))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing 'lat' and 'lon' parameters."}), 400

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT name, address, latitude, longitude, services FROM clinics")
    all_clinics = cursor.fetchall()
    conn.close()

    nearby_clinics = []
    for clinic in all_clinics:
        clinic_dict = dict(clinic)
        dist = haversine_distance(
            user_lat, user_lon,
            clinic_dict['latitude'], clinic_dict['longitude']
        )
        if dist <= radius_km:
            clinic_dict['distance_km'] = round(dist, 2)
            nearby_clinics.append(clinic_dict)

    nearby_clinics.sort(key=lambda x: x['distance_km'])
    return jsonify({"clinics": nearby_clinics})

if __name__ == '__main__':
    app.run(port=5002)