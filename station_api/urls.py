from django.urls import path, include
from rest_framework import routers

from station_api.views import (
    StationViewSet,
    RouteViewSet,
    CrewViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    TripViewSet,
    OrderViewSet
)


router = routers.DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("trips", TripViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "station_api"
