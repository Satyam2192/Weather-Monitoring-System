import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import asyncio

from main import app, periodic_weather_fetch, alert_configs
from app.config import CITIES, OPENWEATHER_API_KEY
from app.utils import fetch_weather_data, calculate_rollups, check_alert_conditions
from app.models import WeatherModel


client = TestClient(app)

def test_fetch_weather():
    response = client.get("/fetch/Delhi")
    assert response.status_code == 200
    data = response.json()
    assert "temp" in data

def test_daily_summary():
    response = client.get("/summary/Delhi")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "avg_temp" in data["summary"]

def test_set_alert():
    response = client.post("/alerts?city=Delhi&threshold=35")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data



@pytest.fixture
def mock_weather_data():
    return {
        "dt": 1729290347,
        "main": {
            "feels_like": 292.15,
            "temp": 293.15
        },
        "weather": [{"main": "Clear"}]
    }


def test_system_setup():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Weather Monitoring System"}
    assert OPENWEATHER_API_KEY is not None and OPENWEATHER_API_KEY != ""

@patch('app.utils.requests.get')
def test_data_retrieval(mock_get, mock_weather_data):
    mock_get.return_value.json.return_value = mock_weather_data
    data = fetch_weather_data("Delhi")
    assert "temp" in data
    assert "feels_like" in data
    assert "condition" in data
    assert "timestamp" in data

@patch('app.utils.requests.get')
def test_temperature_conversion(mock_get, mock_weather_data):
    mock_get.return_value.json.return_value = mock_weather_data
    data = fetch_weather_data("Delhi")
    assert abs(data["temp"] - 20.0) < 0.1  # 293.15K - 273.15 ≈ 20.0C
    assert abs(data["feels_like"] - 19.0) < 0.1  # 292.15K - 273.15 ≈ 19.0C




@patch('app.models.WeatherModel.get_city_data')
def test_daily_weather_summary(mock_get_city_data):
    mock_data = [
        {"temp": 20, "condition": "Clear"},
        {"temp": 22, "condition": "Clear"},
        {"temp": 18, "condition": "Cloudy"},
        {"temp": 21, "condition": "Clear"}
    ]
    mock_get_city_data.return_value = mock_data
    
    response = client.get("/summary/Delhi")
    assert response.status_code == 200
    summary = response.json()["summary"]
    assert summary["avg_temp"] == 20.25
    assert summary["max_temp"] == 22
    assert summary["min_temp"] == 18
    assert summary["dominant_condition"] == "Clear"

def test_alerting_thresholds():
    # Set an alert
    response = client.post("/alerts?city=Delhi&threshold=25")
    assert response.status_code == 200

    # Simulate weather data below threshold
    with patch('app.utils.fetch_weather_data', return_value={"temp": 24, "condition": "Clear"}):
        assert not check_alert_conditions({"temp": 24}, alert_configs["Delhi"].threshold)

    # Simulate weather data above threshold
    with patch('app.utils.fetch_weather_data', return_value={"temp": 26, "condition": "Clear"}):
        assert check_alert_conditions({"temp": 26}, alert_configs["Delhi"].threshold)


if __name__ == "__main__":
    pytest.main()
