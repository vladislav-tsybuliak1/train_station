from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from station_api.models import (
    Station,
    Route,
    Crew,
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


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class CrewReadSerializer(CrewSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta(CrewSerializer.Meta):
        fields = ("id", "full_name", "crew_image")

    def get_full_name(self, obj: Crew) -> str:
        return f"{obj.first_name} {obj.last_name}"


class CrewCreateUpdateSerializer(CrewSerializer):
    class Meta(CrewSerializer.Meta):
        fields = ("id", "first_name", "last_name")


class CrewImageSerializer(CrewSerializer):
    class Meta(CrewSerializer.Meta):
        fields = ("id", "crew_image")
