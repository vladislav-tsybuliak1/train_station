from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from station_api.filters import (
    StationFilter,
    RouteFilter,
    CrewFilter,
    TrainTypeFilter,
)
from station_api.models import Station, Route, Crew, TrainType
from station_api.serializers import (
    StationSerializer,
    RouteSerializer,
    RouteReadSerializer,
    RouteCreateUpdateSerializer,
    CrewSerializer,
    CrewReadSerializer,
    CrewCreateUpdateSerializer,
    CrewImageSerializer,
    TrainTypeSerializer,
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
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    filterset_class = RouteFilter

    def get_serializer_class(self) -> type[RouteSerializer]:
        if self.action in ["list", "retrieve"]:
            return RouteReadSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RouteCreateUpdateSerializer
        return RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filterset_class = CrewFilter

    def get_serializer_class(self) -> type[CrewSerializer]:
        if self.action in ["list", "retrieve"]:
            return CrewReadSerializer
        if self.action in ["create", "update", "partial_update"]:
            return CrewCreateUpdateSerializer
        if self.action == "upload_image":
            return CrewImageSerializer
        return CrewSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(
        self,
        request: Request,
        pk: int | None = None
    ) -> Response:
        """Endpoint for uploading image to specific crew"""
        crew = self.get_object()
        serializer = self.get_serializer(crew, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TrainTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    filterset_class = TrainTypeFilter
