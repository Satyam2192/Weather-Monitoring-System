import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.config import initialize_db, CITIES
from app.utils import fetch_weather_data, calculate_rollups, check_alert_conditions
from app.models import WeatherModel
from app.schemas import WeatherSummary, AlertConfig
from app.visualizations import create_daily_summary_chart, create_historical_trend_chart, create_alert_visualization
from datetime import datetime, timedelta
import logging


alert_configs = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    initialize_db()
    weather_fetch_task = asyncio.create_task(periodic_weather_fetch())
    yield
    # Shutdown
    weather_fetch_task.cancel()
    try:
        await weather_fetch_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

async def periodic_weather_fetch():
    while True:
        for city in CITIES:
            try:
                data = fetch_weather_data(city)
                weather = WeatherModel(city, data["temp"], data["feels_like"], data["condition"], data["timestamp"])
                await weather.save()
                
                if city in alert_configs:
                    if check_alert_conditions(data, alert_configs[city].threshold):
                        print(f"ALERT: Temperature in {city} exceeded {alert_configs[city].threshold}°C!")
            except Exception as e:
                print(f"Error fetching weather for {city}: {str(e)}")
        
        await asyncio.sleep(300)  

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather Monitoring System"}

@app.get("/fetch/{city}")
async def get_weather(city: str):
    if city not in CITIES:
        raise HTTPException(status_code=404, detail="City not found")
    data = fetch_weather_data(city)
    return data

@app.get("/summary/{city}")
async def daily_summary(city: str):
    if city not in CITIES:
        raise HTTPException(status_code=404, detail="City not found")
    
    # weather data for the last 24 hours
    yesterday = datetime.now() - timedelta(days=1)
    weather_data = await WeatherModel.get_city_data(city, yesterday.timestamp())
    
    if not weather_data:
        empty_summary = {"avg_temp": 0, "max_temp": 0, "min_temp": 0, "dominant_condition": "No data"}
        return {"summary": WeatherSummary(**empty_summary), "chart": None}
    
    summary = calculate_rollups(weather_data)
    chart = create_daily_summary_chart(summary)
    return {"summary": WeatherSummary(**summary), "chart": chart}


logging.basicConfig(level=logging.DEBUG)  
logger = logging.getLogger(__name__)

@app.get("/historical/{city}")
async def historical_trend(city: str):
    if city not in CITIES:
        raise HTTPException(status_code=404, detail="City not found")

    # Calculate timestamp for 7 days ago
    week_ago = datetime.now() - timedelta(days=7)
    week_ago_timestamp = week_ago.timestamp()
    
    logger.debug(f"Fetching data for {city} from {week_ago} ({week_ago_timestamp})")
    
    # Fetch weather data from the last 7 days
    weather_data = await WeatherModel.get_city_data(city, week_ago_timestamp)

    if not weather_data:
        logger.warning(f"No historical data available for {city}")
        raise HTTPException(status_code=404, detail="No historical data available")

    logger.info(f"Retrieved {len(weather_data)} data points for {city}")
    logger.debug(f"First data point: {weather_data[0]}")
    logger.debug(f"Last data point: {weather_data[-1]}")
    
    try:
        # Generate and return the historical trend chart
        chart = create_historical_trend_chart(weather_data)
        return {"chart": chart}
    except Exception as e:
        logger.error(f"Error creating chart for {city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating chart")

@app.post("/alerts")
async def set_alert(city: str, threshold: float):
    if city not in CITIES:
        raise HTTPException(status_code=404, detail="City not found")
    alert_configs[city] = AlertConfig(threshold=threshold)
    return {"message": f"Alert set for {city} at {threshold}°C"}

@app.get("/alerts")
def get_alerts():
    return alert_configs

@app.get("/alert_visualization")
def alert_visualization():
    chart = create_alert_visualization(alert_configs)
    return {"chart": chart}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)