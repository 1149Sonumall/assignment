from django.contrib import admin

# Register your models here.
from .models import WeatherForecast
admin.site.register(WeatherForecast)