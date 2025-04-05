from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

location_disaster_data = {
    "uttarakhand": {
        "disaster": "Landslide",
        "risk": "High",
        "precautions": "Avoid hilly areas, stay alert, follow local news."
    },
    "gujarat": {
        "disaster": "Earthquake",
        "risk": "Medium",
        "precautions": "Drop, Cover, and Hold On during tremors."
    },
    "mumbai": {
        "disaster": "Flood",
        "risk": "High",
        "precautions": "Avoid waterlogged areas and stay indoors."
    },
    "rajasthan": {
        "disaster": "Heatwave",
        "risk": "Medium",
        "precautions": "Stay hydrated and avoid outdoor activities."
    },
    "bihar": {
        "disaster": "Flood",
        "risk": "High",
        "precautions": "Move to higher ground and stay alert."
    }
    # Add more locations here...
}

def get_country_from_location(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&addressdetails=1"
    try:
        res = requests.get(url).json()
        return res[0]['address'].get('country', '') if res else ''
    except:
        return ''

def get_reliefweb_disasters(country):
    api_url = f"https://api.reliefweb.int/v1/disasters?appname=apidoc&profile=full&filter[field]=country&filter[value]={country}&sort[]=date:desc&limit=3"
    try:
        res = requests.get(api_url).json()
        disasters = res.get("data", [])
        return [d["fields"]["name"] for d in disasters]
    except:
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    location = data.get('location', '').lower()
    result = location_disaster_data.get(location, {
        "disaster": "Unknown",
        "risk": "Low",
        "precautions": "No major risks reported."
    })

    # Get country and live disaster updates
    country = get_country_from_location(location)
    recent_disasters = get_reliefweb_disasters(country)

    return jsonify({
        "prediction": result['disaster'],
        "risk": result['risk'],
        "precautions": result['precautions'],
        "recent_disasters": recent_disasters
    })

if __name__ == '__main__':
    app.run(debug=True)
