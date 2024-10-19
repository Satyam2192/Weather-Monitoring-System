import requests
from app.config import OPENWEATHER_API_KEY

def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        "temp": data["main"]["temp"] - 273.15,  
        "feels_like": data["main"]["feels_like"] - 273.15,  
        "condition": data["weather"][0]["main"],
        "timestamp": data["dt"]
    }

def calculate_rollups(weather_data):
    temps = [entry['temp'] for entry in weather_data]
    conditions = [entry['condition'] for entry in weather_data]
    dominant_condition = max(set(conditions), key=conditions.count)
    
    return {
        "avg_temp": sum(temps) / len(temps),
        "max_temp": max(temps),
        "min_temp": min(temps),
        "dominant_condition": dominant_condition
    }

def check_alert_conditions(weather_data, threshold):
    if weather_data['temp'] > threshold:
        return True
    return False