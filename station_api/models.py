from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from station_api.validators import validate_latitude, validate_longitude


class Station(models.Model):
    name = models.CharField(max_length=63, unique=True)
    latitude = models.FloatField(validators=[validate_latitude])
    longitude = models.FloatField(validators=[validate_longitude])

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        related_name="source_routes",
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Station,
        related_name="destination_routes",
        on_delete=models.CASCADE
    )

    distance = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"{self.source} - {self.destination}"

    @staticmethod
    def validate_different_stations(
            source: Station,
            destination: Station
    ) -> None:
        if source == destination:
            raise ValidationError(
                "The source and destination stations must be different."
            )

    def clean(self) -> None:
        Route.validate_different_stations(self.source, self.destination)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
