from django.db.models import QuerySet, F, Count
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
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
from station_api.models import (
    Station,
    Route,
    Crew,
    TrainType,
    Train,
    Trip,
    Order
)
from station_api.schemas.crews import crew_set_schema
from station_api.schemas.orders import order_list_create_schema
from station_api.schemas.train_types import (
    train_type_list_create_schema
)
from station_api.schemas.routes import route_set_schema
from station_api.schemas.stations import station_list_create_schema
from station_api.schemas.trains import train_set_schema
from station_api.schemas.trips import trip_set_schema
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
    OrderSerializer,
    OrderListSerializer,
)


@station_list_create_schema
class StationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filterset_class = StationFilter


@route_set_schema
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


@crew_set_schema
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


@train_type_list_create_schema
class TrainTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    filterset_class = TrainTypeFilter


@train_set_schema
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


@trip_set_schema
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
        return queryset.order_by("departure_time")


@order_list_create_schema
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__trip__route__source",
        "tickets__trip__route__destination",
        "tickets__trip__train__train_type",
    )
    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self) -> type[OrderSerializer]:
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer: OrderSerializer):
        serializer.save(user=self.request.user)
