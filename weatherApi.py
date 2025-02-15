from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your OpenWeatherMap API key
API_KEY = "ffc4738f2e3c404ce4151f2365fc4eb4"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# GET weather details for a city
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == '__main__':
    app.run(debug=False)
