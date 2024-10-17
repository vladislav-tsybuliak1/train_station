from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import Order, Ticket, Trip, Train, Route, Station
from station_api.serializers import OrderListSerializer


ORDER_URL = reverse("station-api:order-list")


def detail_url(order_id: int) -> str:
    return reverse("station-api:order-detail", args=[order_id])


class NotAuthenticatedOrderApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
