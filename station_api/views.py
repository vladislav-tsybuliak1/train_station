from rest_framework import mixins, viewsets

from station_api.filters import (
    StationFilter,
)
from station_api.models import Station, Route
from station_api.serializers import (
    StationSerializer,
    RouteSerializer,
    RouteReadSerializer,
    RouteCreateUpdateSerializer
)


class StationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filterset_class = StationFilter


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self) -> type[RouteSerializer]:
        if self.action in ["list", "retrieve"]:
            return RouteReadSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RouteCreateUpdateSerializer
        return RouteSerializer
