from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import Station
from station_api.serializers import StationSerializer
from station_api.views import StationViewSet


STATION_URL = reverse("station-api:station-list")
PAGE_SIZE = StationViewSet.pagination_class.page_size


class NotAuthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(STATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

        self.payload = {
            "name": "Kyiv",
            "latitude": 50.45,
            "longitude": 30.52,
        }

        Station.objects.create(
            name="Chernivtsi",
            latitude=48.29,
            longitude=25.39
        )
        Station.objects.create(name="Donetsk", latitude=48.01, longitude=37.81)
        Station.objects.create(name="Lutsk", latitude=50.76, longitude=25.34)
        Station.objects.create(
            name="Chernihiv",
            latitude=51.50,
            longitude=31.32
        )

    def test_station_list(self) -> None:
        response = self.client.get(STATION_URL)
        stations = Station.objects.all()[:PAGE_SIZE]
        serializer = StationSerializer(stations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_station_filter_by_name(self) -> None:
        name_to_search = "cher"
        response = self.client.get(STATION_URL, {"name": name_to_search})
        stations = (
            Station.objects.filter(name__icontains=name_to_search)[:PAGE_SIZE]
        )
        serializer = StationSerializer(stations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_station_forbidden(self) -> None:
        response = self.client.post(STATION_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.payload = {
            "name": "Kyiv",
            "latitude": 50.45,
            "longitude": 30.52,
        }

    def test_create_station(self) -> None:
        response = self.client.post(STATION_URL, self.payload)
        station = Station.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in self.payload:
            self.assertEqual(self.payload[key], getattr(station, key))

    def test_create_station_with_invalid_latitude_and_longitude(self) -> None:
        self.payload["latitude"] = 100
        self.payload["longitude"] = 100
        response = self.client.post(STATION_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_station_with_same_name(self) -> None:
        response = self.client.post(STATION_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(STATION_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
