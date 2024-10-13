import django_filters

from station_api.models import Station, Route


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
