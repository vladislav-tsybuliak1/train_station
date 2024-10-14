from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from station_api.models import (
    Station,
    Route,
    Crew,
    TrainType,
    Train,
    Trip,
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
    source = serializers.StringRelatedField(read_only=True)
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


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "capacity",
            "train_type",
            "train_image"
        )


class TrainReadSerializer(TrainSerializer):
    train_type = serializers.CharField(
        source="train_type.name",
        read_only=True
    )


class TrainCreateUpdateSerializer(TrainSerializer):
    class Meta(TrainSerializer.Meta):
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type"
        )


class TrainImageSerializer(TrainSerializer):
    class Meta(TrainSerializer.Meta):
        fields = ("id", "train_image")


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class TripListSerializer(TripSerializer):
    route = serializers.StringRelatedField(read_only=True)
    train_name = serializers.CharField(
        source="train.name",
        read_only=True
    )
    train_type = serializers.CharField(
        source="train.train_type",
        read_only=True
    )
    departure_time = serializers.SerializerMethodField()
    arrival_time = serializers.SerializerMethodField()
    train_capacity = serializers.IntegerField(
        source="train.capacity",
        read_only=True,
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta(TripSerializer.Meta):
        fields = (
            "id",
            "route",
            "train_name",
            "train_type",
            "departure_time",
            "arrival_time",
            "train_capacity",
            "tickets_available"
        )

    def get_departure_time(self, obj: Trip) -> str:
        return obj.departure_time.strftime("%d %b %Y %H:%M")

    def get_arrival_time(self, obj: Trip) -> str:
        return obj.arrival_time.strftime("%d %b %Y %H:%M")


class TripRetrieveSerializer(TripListSerializer):
    route = RouteReadSerializer(many=False, read_only=True)
    train = TrainReadSerializer(many=False, read_only=True)
    crew = serializers.SerializerMethodField()

    class Meta(TripSerializer.Meta):
        fields = (
            "id",
            "route",
            "train",
            "departure_time",
            "arrival_time",
            "crew"
        )

    def get_crew(self, obj: Trip) -> list[str]:
        return [
            f"{crew.first_name} {crew.last_name}"
            for crew
            in obj.crew.all()
        ]


class TripCreateUpdateSerializer(TripSerializer):
    class Meta(TripSerializer.Meta):
        fields = (
            "id",
            "route",
            "train",
            "departure_time",
            "arrival_time",
            "crew"
        )

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs=attrs)
        Trip.validate_times(
            departure_time=attrs.get(
                "departure_time",
                self.instance.departure_time if self.instance else None
            ),
            arrival_time=attrs.get(
                "arrival_time",
                self.instance.arrival_time if self.instance else None
            ),
            error_to_raise=ValidationError
        )
        return data
