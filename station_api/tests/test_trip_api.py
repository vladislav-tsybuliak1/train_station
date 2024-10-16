from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import Station, Route, Train, Crew, Trip
from station_api.serializers import TripListSerializer
from station_api.views import TripViewSet


TRIP_URL = reverse("station-api:trip-list")
PAGE_SIZE = TripViewSet.pagination_class.page_size


def detail_url(trip_id: int) -> str:
    return reverse("station-api:trip-detail", args=[trip_id])


class NotAuthenticatedTripApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(TRIP_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
