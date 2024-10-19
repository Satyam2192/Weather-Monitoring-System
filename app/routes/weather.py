from fastapi import APIRouter
from app.utils import fetch_weather_data, calculate_rollups, check_alert_conditions
from app.models import WeatherModel
from app.schemas import WeatherRequest, WeatherSummary

weather_router = APIRouter()

@weather_router.get("/fetch/{city}")
async def fetch_weather(city: str):
    data = fetch_weather_data(city)
    weather = WeatherModel(city, data["temp"], data["feels_like"], data["condition"], data["timestamp"])
    await weather.save()
    return data

@weather_router.get("/summary/{city}")
async def daily_summary(city: str):
    weather_data = await db.weather.find({"city": city}).to_list(100)
    summary = calculate_rollups(weather_data)
    return WeatherSummary(**summary)

@weather_router.post("/alerts")
async def set_alert(city: str, threshold: float):
    latest_weather = await db.weather.find_one({"city": city}, sort=[("timestamp", -1)])
    alert_triggered = check_alert_conditions(latest_weather, threshold)
    if alert_triggered:
        return {"alert": f"Temperature exceeded {threshold} degrees!"}
    return {"message": "No alerts"}
