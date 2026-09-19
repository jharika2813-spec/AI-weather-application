"""OpenWeatherMap integration."""

import os

import requests


class WeatherServiceError(Exception):
    """Raised when weather data cannot be retrieved."""


def get_weather(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherServiceError("OPENWEATHER_API_KEY is not configured.")

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10,
        )
    except requests.RequestException as error:
        raise WeatherServiceError("Weather service is currently unavailable.") from error

    if response.status_code == 404:
        raise WeatherServiceError("City not found. Check the spelling and try again.")
    if not response.ok:
        raise WeatherServiceError("Could not retrieve weather data.")

    data = response.json()
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
    }
