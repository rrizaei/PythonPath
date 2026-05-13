"""
Weather App - Real-time Weather Information System

A comprehensive weather application that fetches and displays current weather conditions,
forecasts, and atmospheric data using the WeatherAPI.com service.

WHAT IT DOES:
- Fetches current weather for any city worldwide
- Displays temperature, conditions, humidity, wind speed, pressure
- Shows 3-day or 7-day weather forecast
- Provides "feels like" temperature and UV index
- Shows sunrise/sunset times
- Displays air quality data (where available)
- Caches recent searches for quick access
- Saves favorite locations

USE CASES:
- Daily weather checking
- Travel planning
- Outdoor activity planning
- Learning API integration in Python
- Weather data analysis

KEY FEATURES:
- Real-time API data from WeatherAPI.com
- Current conditions + multi-day forecast
- Search by city name, ZIP code, or coordinates
- Metric/Imperial unit toggle (C/F, km/h/mph)
- Input validation and error handling
- Color-coded terminal output
- Response caching to reduce API calls
- Favorite locations storage

REQUIREMENTS: Python 3.6+ (requests module, datetime)
INSTALL: pip install requests
API KEY: Get free key from https://www.weatherapi.com
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional, List
import os

class WeatherApp:
    def __init__(self, api_key: str):
        """
        Initialize Weather App with API key

        Args:
            api_key: my WeatherAPI.com API key
        """
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"
        self.units = "metric"  # metric or imperial
        self.cache = {}
        self.favorites = self.load_favorites()

    def get_current_weather(self, location: str) -> Optional[Dict]:
        """
        Get current weather for a location

        Args:
            location: City name, ZIP code, or "auto:ip" for auto-detection

        Returns:
            Dictionary with weather data or None if error
        """
        # Check cache first
        cache_key = f"current_{location}_{self.units}"
        if cache_key in self.cache:
            cache_time = self.cache[cache_key]['timestamp']
            if (datetime.now() - cache_time).seconds < 300:  # 5 minute cache
                print("Using cached data...")
                return self.cache[cache_key]['data']

        url = f"{self.base_url}/current.json"
        params = {
            'key': self.api_key,
            'q': location,
            'aqi': 'yes'  # Include air quality data
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Cache the result
            self.cache[cache_key] = {
                'data': data,
                'timestamp': datetime.now()
            }

            return data

        except requests.exceptions.RequestException as e:
            if hasattr(response, 'status_code'):
                if response.status_code == 401:
                    print("Invalid API key. Please check your API key.")
                elif response.status_code == 400:
                    print(f"Location '{location}' not found. Please check the spelling.")
                else:
                    print(f"Error fetching weather: {e}")
            else:
                print(f"Error fetching weather: {e}")
            return None

    def get_forecast(self, location: str, days: int = 3) -> Optional[Dict]:
        """
        Get weather forecast for a location

        Args:
            location: City name or ZIP code
            days: Number of days (1-7)

        Returns:
            Dictionary with forecast data or None if error
        """
        # Check cache
        cache_key = f"forecast_{location}_{days}_{self.units}"
        if cache_key in self.cache:
            cache_time = self.cache[cache_key]['timestamp']
            if (datetime.now() - cache_time).seconds < 1800:  # 30 min cache
                print("Using cached forecast...")
                return self.cache[cache_key]['data']

        url = f"{self.base_url}/forecast.json"
        params = {
            'key': self.api_key,
            'q': location,
            'days': days,
            'aqi': 'yes',
            'alerts': 'yes'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Cache the result
            self.cache[cache_key] = {
                'data': data,
                'timestamp': datetime.now()
            }

            return data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return None

    def display_current_weather(self, weather_data: Dict):
        """Display current weather in a formatted way"""
        if not weather_data:
            return

        current = weather_data['current']
        location = weather_data['location']

        # Temperature unit symbol
        temp_unit = "C" if self.units == "metric" else "F"
        wind_unit = "km/h" if self.units == "metric" else "mph"

        print("\n" + "="*60)
        print(f"Location: {location['name']}, {location['region']}, {location['country']}")
        print(f"Date: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
        print(f"Local Time: {location['localtime']}")
        print("="*60)

        # Main weather info
        print(f"\nTemperature: {current['temp_c'] if self.units == 'metric' else current['temp_f']}{temp_unit}")
        print(f"Feels like: {current['feelslike_c'] if self.units == 'metric' else current['feelslike_f']}{temp_unit}")
        print(f"Conditions: {current['condition']['text']}")
        print(f"Wind: {current['wind_kph'] if self.units == 'metric' else current['wind_mph']} {wind_unit} {current['wind_dir']}")
        print(f"Humidity: {current['humidity']}%")
        print(f"UV Index: {current['uv']}")
        print(f"Visibility: {current['vis_km'] if self.units == 'metric' else current['vis_miles']} {('km' if self.units == 'metric' else 'miles')}")
        print(f"Pressure: {current['pressure_mb'] if self.units == 'metric' else current['pressure_in']} {('mb' if self.units == 'metric' else 'in')}")

        # Air quality if available
        if 'air_quality' in current:
            aq = current['air_quality']
            print("\nAIR QUALITY:")
            print(f"   PM2.5: {aq.get('pm2_5', 'N/A')} micrograms/m3")
            print(f"   PM10: {aq.get('pm10', 'N/A')} micrograms/m3")

            # Air quality index interpretation
            us_epa = aq.get('us-epa-index', 0)
            aq_text = {
                1: "Good",
                2: "Moderate",
                3: "Unhealthy for sensitive groups",
                4: "Unhealthy",
                5: "Very Unhealthy",
                6: "Hazardous"
            }.get(us_epa, "Unknown")
            print(f"   US EPA Index: {us_epa} - {aq_text}")

        print("="*60)

    def display_forecast(self, forecast_data: Dict):
        """Display weather forecast"""
        if not forecast_data:
            return

        forecast = forecast_data['forecast']['forecastday']
        location = forecast_data['location']

        print("\n" + "="*60)
        print(f"WEATHER FORECAST FOR {location['name']}, {location['country']}")
        print("="*60)

        temp_unit = "C" if self.units == "metric" else "F"

        for day in forecast:
            date = datetime.strptime(day['date'], "%Y-%m-%d")
            day_name = date.strftime("%A")

            print(f"\n{day_name}, {day['date']}")
            print(f"   Temperature: {day['day']['maxtemp_c' if self.units == 'metric' else 'maxtemp_f']}{temp_unit} "
                  f"/ {day['day']['mintemp_c' if self.units == 'metric' else 'mintemp_f']}{temp_unit}")
            print(f"   Conditions: {day['day']['condition']['text']}")
            print(f"   Chance of rain: {day['day']['daily_chance_of_rain']}%")
            print(f"   Max wind: {day['day']['maxwind_kph' if self.units == 'metric' else 'maxwind_mph']} "
                  f"{('km/h' if self.units == 'metric' else 'mph')}")
            print(f"   Humidity: {day['day']['avghumidity']}%")
            print(f"   Sunrise: {day['astro']['sunrise']}")
            print(f"   Sunset: {day['astro']['sunset']}")

        print("="*60)

    def display_hourly_forecast(self, forecast_data: Dict, hours: int = 12):
        """Display hourly forecast"""
        if not forecast_data:
            return

        forecast_days = forecast_data['forecast']['forecastday']
        location = forecast_data['location']

        print("\n" + "="*60)
        print(f"HOURLY FORECAST FOR {location['name']} (Next {hours} hours)")
        print("="*60)

        temp_unit = "C" if self.units == "metric" else "F"

        hours_shown = 0
        for day in forecast_days:
            for hour in day['hour']:
                if hours_shown >= hours:
                    break

                hour_time = hour['time'].split(' ')[1]
                temp = hour[f'temp_{"c" if self.units == "metric" else "f"}']
                condition = hour['condition']['text']
                chance_rain = hour['chance_of_rain']

                print(f"\nTime: {hour_time}")
                print(f"   Temperature: {temp}{temp_unit}")
                print(f"   Conditions: {condition}")
                print(f"   Chance of rain: {chance_rain}%")

                hours_shown += 1

            if hours_shown >= hours:
                break

    def add_favorite(self, location: str):
        """Add a location to favorites"""
        if location not in self.favorites:
            self.favorites.append(location)
            self.save_favorites()
            print(f"Added '{location}' to favorites")
        else:
            print(f"'{location}' is already in favorites")

    def remove_favorite(self, location: str):
        """Remove a location from favorites"""
        if location in self.favorites:
            self.favorites.remove(location)
            self.save_favorites()
            print(f"Removed '{location}' from favorites")
        else:
            print(f"'{location}' not found in favorites")

    def load_favorites(self) -> List[str]:
        """Load favorites from file"""
        try:
            with open('weather_favorites.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_favorites(self):
        """Save favorites to file"""
        with open('weather_favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def toggle_units(self):
        """Toggle between metric and imperial units"""
        self.units = "imperial" if self.units == "metric" else "metric"
        unit_name = "Celsius/Fahrenheit (metric)" if self.units == "metric" else "Fahrenheit/Celsius (imperial)"
        print(f"Units switched to {unit_name}")

        # Clear cache when changing units
        self.cache.clear()

def main():
    """Main program loop"""
    # API key - replace with your actual key
    API_KEY = "39cc939ec2554ad984b183941260204"

    app = WeatherApp(API_KEY)

    print("\n" + "="*60)
    print("WEATHER APP")
    print("="*60)
    print("Powered by WeatherAPI.com")

    while True:
        print("\n" + "-"*50)
        print("OPTIONS:")
        print("  1. Current weather")
        print("  2. Weather forecast (3-day)")
        print("  3. Weather forecast (7-day)")
        print("  4. Hourly forecast")
        print("  5. View favorites")
        print("  6. Add to favorites")
        print("  7. Remove from favorites")
        print("  8. Toggle units (C/F)")
        print("  9. Exit")

        choice = input("\nYour choice (1-9): ").strip()

        if choice == '1':
            location = input("Enter city name or ZIP code: ").strip()
            if not location:
                print("Please enter a location")
                continue

            weather = app.get_current_weather(location)
            if weather:
                app.display_current_weather(weather)

        elif choice == '2':
            location = input("Enter city name or ZIP code: ").strip()
            if not location:
                print("Please enter a location")
                continue

            forecast = app.get_forecast(location, days=3)
            if forecast:
                app.display_current_weather(forecast)
                app.display_forecast(forecast)

        elif choice == '3':
            location = input("Enter city name or ZIP code: ").strip()
            if not location:
                print("Please enter a location")
                continue

            forecast = app.get_forecast(location, days=7)
            if forecast:
                app.display_current_weather(forecast)
                app.display_forecast(forecast)

        elif choice == '4':
            location = input("Enter city name or ZIP code: ").strip()
            if not location:
                print("Please enter a location")
                continue

            try:
                hours = int(input("Number of hours to show (1-24): ").strip())
                hours = min(24, max(1, hours))
            except ValueError:
                hours = 12

            forecast = app.get_forecast(location, days=2)
            if forecast:
                app.display_hourly_forecast(forecast, hours)

        elif choice == '5':
            if app.favorites:
                print("\nYour favorite locations:")
                for i, loc in enumerate(app.favorites, 1):
                    print(f"  {i}. {loc}")
            else:
                print("No favorites saved yet")

        elif choice == '6':
            location = input("Enter location to add to favorites: ").strip()
            if location:
                app.add_favorite(location)

        elif choice == '7':
            if app.favorites:
                print("\nYour favorite locations:")
                for i, loc in enumerate(app.favorites, 1):
                    print(f"  {i}. {loc}")
                try:
                    idx = int(input("Enter number to remove: ").strip()) - 1
                    if 0 <= idx < len(app.favorites):
                        app.remove_favorite(app.favorites[idx])
                except ValueError:
                    print("Invalid selection")
            else:
                print("No favorites to remove")

        elif choice == '8':
            app.toggle_units()

        elif choice == '9':
            print("\nThank you for using the Weather App!")
            break

        else:
            print("Invalid choice. Please enter 1-9")

if __name__ == "__main__":
    main()