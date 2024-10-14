import django_filters
from django.db.models import Q, QuerySet

from station_api.models import Station, Route, Crew, TrainType


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
