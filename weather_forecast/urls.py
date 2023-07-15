# weather_forecast/urls.py

from django.urls import path
from .views import WeatherForecastView, index, forecast

urlpatterns = [
    path('', index, name='index'),
    path('forecast/', forecast, name='forecast'),
    path('api/weather-forecast/', WeatherForecastView.as_view(), name='weather-forecast'),
]
