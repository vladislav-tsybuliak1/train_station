from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from station_api.filters import (
    StationFilter,
)
from station_api.models import Station
from station_api.serializers import StationSerializer


class StationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filterset_class = StationFilter
