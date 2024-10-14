from django.db.models import QuerySet, F, Count
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from station_api.filters import (
    StationFilter,
    RouteFilter,
    CrewFilter,
    TrainTypeFilter,
    TrainFilter,
    TripFilter,
)
from station_api.models import Station, Route, Crew, TrainType, Train, Trip
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
    TrainSerializer,
    TrainReadSerializer,
    TrainCreateUpdateSerializer,
    TrainImageSerializer,
    TripSerializer,
    TripCreateUpdateSerializer,
    TripListSerializer,
    TripRetrieveSerializer,
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
    filterset_class = RouteFilter

    def get_serializer_class(self) -> type[RouteSerializer]:
        if self.action in ["list", "retrieve"]:
            return RouteReadSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RouteCreateUpdateSerializer
        return RouteSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("source", "destination")
        return queryset


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


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    filterset_class = TrainFilter

    def get_serializer_class(self) -> type[TrainSerializer]:
        if self.action in ["list", "retrieve"]:
            return TrainReadSerializer
        if self.action in ["create", "update", "partial_update"]:
            return TrainCreateUpdateSerializer
        if self.action == "upload_image":
            return TrainImageSerializer
        return TrainSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if self.action in ["list", "retrieve"]:
            queryset = queryset.select_related("train_type")
        return queryset

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
        """Endpoint for uploading image to specific train"""
        train = self.get_object()
        serializer = self.get_serializer(train, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TripViewSet(viewsets.ModelViewSet):
    queryset = (
        Trip.objects
        .select_related(
            "route__source",
            "route__destination",
            "train__train_type"
        )
    )
    serializer_class = TripSerializer
    filterset_class = TripFilter

    def get_serializer_class(self) -> type[TripSerializer]:
        if self.action == "list":
            return TripListSerializer
        if self.action == "retrieve":
            return TripRetrieveSerializer
        if self.action in ["create", "update", "partial_update"]:
            return TripCreateUpdateSerializer
        return TripSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.annotate(
                tickets_available=(
                    F("train__cargo_num")
                    * F("train__places_in_cargo")
                    - Count("tickets")
                )
            )
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("crew")
        return queryset
