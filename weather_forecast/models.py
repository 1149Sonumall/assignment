
# weather_forecast/models.py

from django.db import models

class WeatherForecast(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    detailing_type = models.CharField(max_length=20)
    forecast_data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lat: {self.lat}, Lon: {self.lon}"
