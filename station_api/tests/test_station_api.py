from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


STATION_URL = reverse("station-api:station-list")


class NotAuthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(STATION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
