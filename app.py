from flask import Flask, request
from geopy.geocoders import Nominatim
import datetime

app = Flask(__name__)
geolocator = Nominatim(user_agent="location-tracker")

# State to Region Map
state_region_map = {
    "Jammu and Kashmir": "Northern", "Punjab": "Northern", "Haryana": "Northern",
    "Uttar Pradesh": "Northern", "Himachal Pradesh": "Northern", "Uttarakhand": "Northern",
    "Rajasthan": "Western", "Gujarat": "Western", "Maharashtra": "Western", "Goa": "Western",
    "Madhya Pradesh": "Central", "Chhattisgarh": "Central", "Bihar": "Eastern", "Jharkhand": "Eastern",
    "West Bengal": "Eastern", "Odisha": "Eastern", "Assam": "Northeastern", "Meghalaya": "Northeastern",
    "Manipur": "Northeastern", "Mizoram": "Northeastern", "Nagaland": "Northeastern",
    "Tripura": "Northeastern", "Arunachal Pradesh": "Northeastern", "Sikkim": "Northeastern",
    "Tamil Nadu": "Southern", "Kerala": "Southern", "Andhra Pradesh": "Southern",
    "Karnataka": "Southern", "Telangana": "Southern"
}

@app.route('/save-location', methods=['POST'])
def save_location():
    data = request.json
    lat = data.get('latitude')
    lon = data.get('longitude')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        location = geolocator.reverse((lat, lon), language='en')
        address = location.raw.get('address', {})
        state = address.get('state', 'Unknown')
        region = state_region_map.get(state, 'Unknown Region')

        with open("locations.txt", "a") as f:
            f.write(f"{timestamp} - {state}, {region} Region, India (Lat: {lat}, Lon: {lon})\n")

        return {'status': 'Location saved', 'state': state, 'region': region}, 200

    except Exception as e:
        return {'status': 'Error in location lookup', 'error': str(e)}, 500

@app.route('/')
def home():
    return "✅ Location Tracking API is Running"

