import matplotlib.pyplot as plt
import io
import base64
import matplotlib.dates as mdates
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_daily_summary_chart(summary):
    fig, ax = plt.subplots()
    ax.bar(['Average', 'Maximum', 'Minimum'], [summary['avg_temp'], summary['max_temp'], summary['min_temp']])
    ax.set_ylabel('Temperature (°C)')
    ax.set_title(f'Daily Temperature Summary\nDominant condition: {summary["dominant_condition"]}')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()

def create_historical_trend_chart(weather_data):
    if not weather_data:
        raise ValueError("No weather data available")

    # Extract timestamps and temperatures from the data
    timestamps = [datetime.fromtimestamp(entry['timestamp']) for entry in weather_data]
    temperatures = [entry['temp'] for entry in weather_data]

    logger.debug(f"Creating chart with {len(timestamps)} data points")
    logger.debug(f"First timestamp: {timestamps[0]}, Last timestamp: {timestamps[-1]}")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(timestamps, temperatures, marker='o', linestyle='-', color='blue')

    # Format the x-axis to show dates for the last 7 days
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)

    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title(f'Historical Temperature Trend for {weather_data[0]["city"]}')

    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.7)

    # Adjust y-axis to show a reasonable range
    if len(temperatures) > 1:
        temp_range = max(temperatures) - min(temperatures)
        ax.set_ylim(min(temperatures) - 0.1 * temp_range, max(temperatures) + 0.1 * temp_range)

    # Ensure x-axis shows full range of dates
    ax.set_xlim(min(timestamps), max(timestamps))

    # Tight layout to ensure everything fits
    plt.tight_layout()

    # Save the figure to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Close the plot to free up memory
    plt.close(fig)

    # Return base64 encoded image
    return base64.b64encode(buffer.getvalue()).decode()


def create_alert_visualization(alert_configs):
    cities = list(alert_configs.keys())
    thresholds = [config.threshold for config in alert_configs.values()]
    
    fig, ax = plt.subplots()
    ax.bar(cities, thresholds)
    ax.set_ylabel('Alert Threshold (°C)')
    ax.set_title('Alert Thresholds by City')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()