from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from station_api.models import (
    Station,
    Route,
)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteReadSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(
        source="destination.name",
        read_only=True
    )


class RouteCreateUpdateSerializer(RouteSerializer):
    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs=attrs)
        Route.validate_different_stations(
            source=attrs.get(
                "source",
                self.instance.source if self.instance else None
            ),
            destination=attrs.get(
                "destination",
                self.instance.destination if self.instance else None
            ),
            error_to_raise=ValidationError
        )
        return data
