# File: /home/sk/Desktop/Zeotap/weather-monitoring/app/models.py

from app.config import db
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WeatherModel:
    def __init__(self, city, temp, feels_like, condition, timestamp):
        self.city = city
        self.temp = temp
        self.feels_like = feels_like
        self.condition = condition
        self.timestamp = timestamp

    async def save(self):
        await db.weather.insert_one(self.__dict__)

    @classmethod
    async def get_city_data(cls, city: str, start_time: float):
        logger.debug(f"Fetching data for {city} from {datetime.fromtimestamp(start_time)}")
        # Fetch data where city matches and timestamp is greater than start_time (last 7 days)
        cursor = db.weather.find({
            "city": city, 
            "timestamp": {"$gte": start_time}
        }).sort("timestamp", 1)
        
        data = await cursor.to_list(None)
        logger.debug(f"Found {len(data)} records for {city}")
        return data

    @classmethod
    async def get_latest_data(cls, city: str):
        return await db.weather.find_one({"city": city}, sort=[("timestamp", -1)])