from django.urls import path, include
from rest_framework import routers

from station_api.views import (
    StationViewSet,
    RouteViewSet,
    CrewViewSet
)


router = routers.DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "station_api"
