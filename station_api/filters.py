import django_filters

from station_api.models import Station


class StationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Station
        fields = ("name",)
