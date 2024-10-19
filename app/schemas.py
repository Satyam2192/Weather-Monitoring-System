from pydantic import BaseModel

class WeatherRequest(BaseModel):
    city: str
    temp: float
    feels_like: float
    condition: str
    timestamp: int

class WeatherSummary(BaseModel):
    avg_temp: float
    max_temp: float
    min_temp: float
    dominant_condition: str

class AlertConfig(BaseModel):
    threshold: float