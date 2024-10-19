


# Weather Monitoring System

This project implements a real-time data processing system for weather monitoring with rollups and aggregates. It utilizes the OpenWeatherMap API to fetch weather data for major Indian cities and provides summarized insights.

## Features

- Real-time weather data fetching for Delhi, Mumbai, Chennai, Bangalore, Kolkata, and Hyderabad
- Daily weather summaries with average, maximum, and minimum temperatures, and dominant weather condition
- Historical weather trends
- Configurable temperature alerts
- Data visualization for summaries, trends, and alerts

## Setup and Installation

1.Create a virtual environment and activate it:
   ```
   python3 -m venv .venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2.Install the required packages:
```
pip install -r requirements.txt
````

3. Run the application:
```
uvicorn main:app --reload
```
4. Run the tests:
```
pytest tests/test_weather.py
```

### With Docker

1. Clone the repository:
   ```
   git clone https://github.com/your-username/weather-monitoring-system.git
   cd weather-monitoring-system
   ```

2. Create a `.env` file in the project root and add your MongoDB URI and OpenWeatherMap API key:
   ```
   MONGO_URI=your_mongodb_uri
   OPENWEATHER_API_KEY=your_api_key
   ```

3. Build and run the Docker container:
   ```
   docker build -t weather-monitoring .
   docker run -p 8000:8000 weather-monitoring
   ```

## API Endpoints

- GET `/weather/{city}`: Get current weather for a city
- GET `/summary/{city}`: Get daily weather summary for a city
- GET `/historical/{city}`: Get historical weather trend for a city
- POST `/set_alert/{city}`: Set temperature alert for a city
- GET `/alerts`: Get all configured alerts
- GET `/alert_visualization`: Get visualization of all alert thresholds

## Design Choices

- FastAPI for high-performance asynchronous API
- MongoDB for efficient storage and retrieval of weather data
- Asynchronous background task for periodic weather data fetching
- Matplotlib for generating visualizations
- Docker for easy deployment and scalability

## Dependencies

All required dependencies are listed in `requirements.txt` and will be installed when building the Docker image. Key dependencies include:

- FastAPI
- Uvicorn
- Motor (asynchronous MongoDB driver)
- Pydantic
- Requests
- Python-dotenv
- Matplotlib

## Future Improvements

- Implement email notifications for alerts
- Add more sophisticated data analysis and prediction features
- Enhance visualizations with interactive charts
- Implement user authentication for personalized alerts and preferences