import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.weather_db

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

def initialize_db():
    print("MongoDB connected successfully.")