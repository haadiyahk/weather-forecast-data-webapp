import os
from dotenv import load_dotenv
import requests

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_data(place, forecast_days=None, kind=None): 
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()

    filtered_data = data["list"]
    number_days = forecast_days * 8  
    filtered_data = filtered_data[:number_days]

    if kind == "Temperature":
        filtered_data = [dict["main"]["temp"] for dict in filtered_data]
    if kind == "Sky":
        filtered_data = [dict["weather"][0]["main"] for dict in filtered_data]
    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Tokyo", forecast_days=3, kind="Temperature"))