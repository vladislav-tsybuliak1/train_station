from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import Station, Route
from station_api.serializers import (
    RouteReadSerializer,
    RouteCreateUpdateSerializer
)
from station_api.views import RouteViewSet


ROUTE_URL = reverse("station-api:route-list")
PAGE_SIZE = RouteViewSet.pagination_class.page_size


def detail_url(route_id: int) -> str:
    return reverse("station-api:route-detail", args=[route_id])


class NotAuthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

        self.station_1 = Station.objects.create(
            name="Chernivtsi",
            latitude=48.29,
            longitude=25.39
        )
        self.station_2 = Station.objects.create(
            name="Donetsk",
            latitude=48.01,
            longitude=37.81
        )
        self.station_3 = Station.objects.create(
            name="Chernihiv",
            latitude=51.50,
            longitude=31.32
        )

        self.route_1 = Route.objects.create(
            source=self.station_1,
            destination=self.station_3,
            distance=600
        )
        self.route_2 = Route.objects.create(
            source=self.station_2,
            destination=self.station_3,
            distance=400
        )
        self.route_3 = Route.objects.create(
            source=self.station_1,
            destination=self.station_2,
            distance=950
        )
        self.route_4 = Route.objects.create(
            source=self.station_2,
            destination=self.station_1,
            distance=950
        )

        self.payload = {
            "source": self.station_3.id,
            "destination": self.station_1.id,
            "distance": 600
        }

    def test_route_list(self) -> None:
        response = self.client.get(ROUTE_URL)
        routes = Route.objects.all()
        serializer = RouteReadSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_route_by_source(self) -> None:
        name_to_search = "chernivtsi"
        response = self.client.get(ROUTE_URL, {"source": name_to_search})
        routes = (
            Route.objects.filter(
                source__name__icontains=name_to_search
            )[:PAGE_SIZE]
        )
        serializer = RouteReadSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_route_by_destination(self) -> None:
        name_to_search = "chernivtsi"
        response = self.client.get(ROUTE_URL, {"destination": name_to_search})
        routes = (
            Route.objects.filter(
                destination__name__icontains=name_to_search
            )[:PAGE_SIZE]
        )
        serializer = RouteReadSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_route_forbidden(self) -> None:
        response = self.client.post(ROUTE_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_route(self) -> None:
        route = self.route_1
        response = self.client.get(detail_url(route.id))
        serializer = RouteReadSerializer(route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_route_forbidden(self) -> None:
        response = self.client.put(detail_url(self.route_1.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_route_forbidden(self) -> None:
        response = self.client.patch(detail_url(self.route_1.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_route_forbidden(self) -> None:
        response = self.client.delete(detail_url(self.route_1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
