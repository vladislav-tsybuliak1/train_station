from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from station_api.validators import (
    validate_latitude,
    validate_longitude,
    validate_name
)


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
        to=Station,
        related_name="source_routes",
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        to=Station,
        related_name="destination_routes",
        on_delete=models.CASCADE
    )

    distance = models.FloatField(validators=[MinValueValidator(0)])

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


class Crew(models.Model):
    first_name = models.CharField(max_length=63, validators=[validate_name])
    last_name = models.CharField(max_length=63, validators=[validate_name])

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class TrainType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.PositiveSmallIntegerField()
    places_in_cargo = models.PositiveSmallIntegerField()
    train_type = models.ForeignKey(
        to=TrainType,
        related_name="trains",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name

    @property
    def capacity(self) -> int:
        return self.cargo_num * self.places_in_cargo


class Trip(models.Model):
    route = models.ForeignKey(
        to=Route,
        related_name="trips",
        on_delete=models.CASCADE
    )
    train = models.ForeignKey(
        to=Train,
        related_name="trips",
        on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        to=Crew,
        related_name="trips"
    )

    def __str__(self) -> str:
        return f"Trip {self.route} ({self.departure_time}-{self.arrival_time})"

    @staticmethod
    def validate_times(
        departure_time: datetime,
        arrival_time: datetime
    ) -> None:
        if departure_time >= arrival_time:
            raise ValidationError(
                "Departure time must be before arrival time.")

    @staticmethod
    def validate_train_not_overlapping(
        train: Train,
        departure_time: datetime,
        arrival_time: datetime
    ) -> None:
        overlapping_trips = Trip.objects.filter(
            train=train,
            departure_time__lt=arrival_time,
            arrival_time__gt=departure_time
        )

        if overlapping_trips.exists():
            raise ValidationError(
                "The train is assigned to overlapping trips."
            )

    @staticmethod
    def validate_crew_not_overlapping(
        crew: list[Crew],
        departure_time: datetime,
        arrival_time: datetime,
    ) -> None:
        overlapping_trips = Trip.objects.filter(
            crew__in=crew,
            departure_time__lt=arrival_time,
            arrival_time__gt=departure_time
        ).distinct()

        if overlapping_trips.exists():
            raise ValidationError(
                "A crew cannot be assigned to overlapping trips."
            )

    def clean(self) -> None:
        Trip.validate_times(
            departure_time=self.departure_time,
            arrival_time=self.arrival_time
        )
        Trip.validate_train_not_overlapping(
            train=self.train,
            departure_time=self.departure_time,
            arrival_time=self.arrival_time
        )
        Trip.validate_crew_not_overlapping(
            crew=self.crew,
            departure_time=self.departure_time,
            arrival_time=self.arrival_time,
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
