import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# CURRENT WEATHER
def get_current_weather(place):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "main" not in data:
        raise ValueError("City not found")

    return data


# FORECAST DATA
def get_data(place, days): 
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={WEATHER_API_KEY}&units=metric"
    
    response = requests.get(url)
    data = response.json()

    # Raise an error if city doesn't exist
    if "list" not in data:
        raise ValueError("City not found")

    forecast_list = data["list"]

    today = datetime.now().date()

    filtered_data = []

    for item in forecast_list:

        forecast_date = datetime.strptime(
            item["dt_txt"],
            "%Y-%m-%d %H:%M:%S"
        ).date()

        # TODAY
        if days == 0:  # If the user selects "Today"
            if forecast_date == today:  # Include only forecasts for today
                filtered_data.append(item)

        # TOMORROW ONWARDS
        else:
            start_date = today + timedelta(days=1) 
            # if user selects anything other than today, we want to start from tomorrow, hence +1
            # datetime.timedelta is used to represent a duration or the difference between two dates or times

            end_date = start_date + timedelta(days=days)

            if start_date <= forecast_date < end_date: #Include forecasts on or after start_date. Exclude forecasts on or after end_date
                filtered_data.append(item)

    return filtered_data


if __name__ == "__main__":
    print(get_current_weather("Mumbai"))
    print(get_data("Mumbai", 2))