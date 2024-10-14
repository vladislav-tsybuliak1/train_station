from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models

from station_api.utils import train_image_file_path, crew_image_file_path
from station_api.validators import (
    validate_latitude,
    validate_longitude,
    validate_name, validate_image_size
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "destination"],
                name="unique_source_destination"
            )
        ]

    def __str__(self) -> str:
        return f"{self.source} - {self.destination}"

    @staticmethod
    def validate_different_stations(
        source: Station,
        destination: Station,
        error_to_raise: type[Exception]
    ) -> None:
        if source == destination:
            raise error_to_raise(
                "The source and destination stations must be different."
            )

    def clean(self) -> None:
        Route.validate_different_stations(
            source=self.source,
            destination=self.destination,
            error_to_raise=ValidationError
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class Crew(models.Model):
    first_name = models.CharField(max_length=63, validators=[validate_name])
    last_name = models.CharField(max_length=63, validators=[validate_name])
    crew_image = models.ImageField(
        null=True,
        upload_to=crew_image_file_path,
        validators=[
            validate_image_size,
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ]
    )

    class Meta:
        ordering = ("first_name", "last_name")

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
    train_image = models.ImageField(
        null=True,
        upload_to=train_image_file_path,
        validators=[
            validate_image_size,
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ]
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
        related_name="trips",
        blank=True
    )

    class Meta:
        ordering = ("departure_time",)

    def __str__(self) -> str:
        return f"Trip {self.route} ({self.departure_time}-{self.arrival_time})"

    @staticmethod
    def validate_times(
        departure_time: datetime,
        arrival_time: datetime,
        error_to_raise: type[Exception],
    ) -> None:
        if departure_time >= arrival_time:
            raise error_to_raise(
                "Departure time must be before arrival time.")

    def clean(self) -> None:
        Trip.validate_times(
            departure_time=self.departure_time,
            arrival_time=self.arrival_time,
            error_to_raise=ValidationError
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    cargo = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()
    trip = models.ForeignKey(
        to=Trip,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        to=Order,
        related_name="tickets",
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cargo", "seat", "trip"],
                name="unique_cargo_seat_trip"
            )
        ]
        ordering = ("trip", "cargo", "seat")

    def __str__(self) -> str:
        return f"{self.trip} - (cargo: {self.cargo}, seat: {self.seat}"

    @staticmethod
    def validate_ticket(
        cargo: int,
        seat: int,
        train: Train,
        error_to_raise: type[Exception]
    ) -> None:
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (cargo, "cargo", "cargo_num"),
            (seat, "seat", "places_in_cargo"),
        ]:
            count_attr = getattr(train, train_attr_name)
            if not (1 <= ticket_attr_value <= count_attr):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in this range: "
                                          f"(1, {train_attr_name}): "
                                          f"(1, {count_attr})"
                    }
                )

    def clean(self) -> None:
        Ticket.validate_ticket(
            cargo=self.cargo,
            seat=self.seat,
            train=self.trip.train,
            error_to_raise=ValidationError,
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
