import datetime
import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    API_KEY = open("D:\\weather-d\\weather_project\\weather_app\\API_KEYS", "r").read()

    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"
    


    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)  # Corrected way to get city2

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2,
        }

        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    
    if "coord" not in response:
        return None, None  # Return None if city is invalid

    try:
        lat, lon = response['coord']['lat'], response['coord']['lon']
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

        weather_data = {
            "city": city,
            "temperature": round(response['main']['temp'] - 273.15, 2),
            "description": response['weather'][0]['description'],
            "icon": response['weather'][0]['icon']
        }

        daily_forecasts = []
        for daily_data in forecast_response.get('daily', [])[:3]:
            daily_forecasts.append({
                "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
                "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
                "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
                "description": daily_data['weather'][0]['description'],
                "icon": daily_data['weather'][0]['icon']
            })

        return weather_data, daily_forecasts
    except KeyError:
        return None, None  # Handle missing keys safely

