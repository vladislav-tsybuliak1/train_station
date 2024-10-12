from django.db import models

from station_api.validators import validate_latitude, validate_longitude


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField(validators=[validate_latitude])
    longitude = models.FloatField(validators=[validate_longitude])

    def __str__(self) -> str:
        return self.name
