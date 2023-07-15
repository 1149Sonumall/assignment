from django.shortcuts import render



from rest_framework import generics
from .models import WeatherForecast
from .serializers import WeatherForecastSerializer
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import datetime

class WeatherForecastView(generics.RetrieveAPIView):
    serializer_class = WeatherForecastSerializer

    def get_object(self):
        lat = float(self.request.query_params.get('lat'))
        lon = float(self.request.query_params.get('lon'))
        detailing_type = self.request.query_params.get('detailing_type')

        # Check if data exists in the local DB
        weather_forecast = WeatherForecast.objects.filter(
            lat=lat, lon=lon, detailing_type=detailing_type
        ).first()

        if weather_forecast:
            last_updated = weather_forecast.last_updated
            threshold = settings.DATA_FRESHNESS_THRESHOLD  # Time sensitivity threshold (in minutes)
            now = datetime.datetime.now()
            time_difference = (now - last_updated).total_seconds() / 60

            if time_difference <= threshold:
                return weather_forecast

        # Fetch data from OpenWeatherMap API
        # api_key = '20fe5d39b77194b6f8acf0adca657a7d'
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid={'c29b62628fdbf89c0027e9781670e133'}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            forecast_data = response.json()

            # Save data to the local DB
            if weather_forecast:
                weather_forecast.forecast_data = forecast_data
                weather_forecast.save()
            else:
                weather_forecast = WeatherForecast.objects.create(
                    lat=lat,
                    lon=lon,
                    detailing_type=detailing_type,
                    forecast_data=forecast_data
                )

            return weather_forecast

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather forecast data: {e}")

        return None

def index(request):
    return render(request, 'index.html')

def forecast(request):
    if request.method == 'POST':
        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))
        detailing_type = request.POST.get('detailing_type')

        # Redirect to the weather forecast view with query parameters
        return redirect(f'/api/weather-forecast/?lat={lat}&lon={lon}&detailing_type={detailing_type}')

    return redirect('/')
