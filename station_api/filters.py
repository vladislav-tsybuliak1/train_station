import django_filters
from django.db.models import (
    Q,
    F,
    Count,
    ExpressionWrapper,
    QuerySet,
    IntegerField,
)

from station_api.models import Station, Route, Crew, TrainType, Train, Trip


class StationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Station
        fields = ("name",)


class RouteFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(
        field_name="source__name",
        lookup_expr="icontains"
    )
    destination = django_filters.CharFilter(
        field_name="destination__name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Route
        fields = ("source", "destination")


class CrewFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method="filter_by_full_name")

    class Meta:
        model = Crew
        fields = ["full_name"]

    def filter_by_full_name(self, queryset, name, value) -> QuerySet:
        names = value.split()
        if len(names) == 2:
            first_name, last_name = names
            return queryset.filter(
                Q(first_name__icontains=first_name)
                & Q(last_name__icontains=last_name)
            )
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )


class TrainTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = TrainType
        fields = ("name",)


class TrainFilter(django_filters.FilterSet):
    capacity_min = django_filters.NumberFilter(method="filter_capacity_min")
    capacity_max = django_filters.NumberFilter(method="filter_capacity_max")
    train_type_name = django_filters.CharFilter(
        field_name="train_type__name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Train
        fields = ("train_type_name",)

    def filter_capacity_min(self, queryset, name, value) -> QuerySet:
        return queryset.annotate(
            annotated_capacity=ExpressionWrapper(
                F("cargo_num") * F("places_in_cargo"),
                output_field=IntegerField()
            )
        ).filter(annotated_capacity__gte=value)

    def filter_capacity_max(self, queryset, name, value) -> QuerySet:
        return queryset.annotate(
            annotated_capacity=ExpressionWrapper(
                F("cargo_num") * F("places_in_cargo"),
                output_field=IntegerField()
            )
        ).filter(annotated_capacity__lte=value)


class TripFilter(django_filters.FilterSet):
    departure_date = django_filters.DateFilter(
        field_name="departure_time",
        lookup_expr="date"
    )
    source_station = django_filters.CharFilter(
        field_name="route__source__name",
        lookup_expr="iexact"
    )
    destination_station = django_filters.CharFilter(
        field_name="route__destination__name",
        lookup_expr="iexact"
    )
    tickets_available = django_filters.BooleanFilter(
        method="filter_tickets_available"
    )
    train_type = django_filters.CharFilter(
        field_name="train__train_type__name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Trip
        fields = (
            "departure_date",
            "source_station",
            "destination_station",
            "tickets_available",
            "train_type"
        )

    def filter_tickets_available(self, queryset, name, value) -> QuerySet:
        if value:
            return queryset.annotate(
                tickets_available=(
                    F("train__cargo_num")
                    * F("train__places_in_cargo")
                    - Count("tickets")
                )
            ).filter(tickets_available__gt=0)
        return queryset
