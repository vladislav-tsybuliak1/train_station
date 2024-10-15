from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.views import TrainViewSet


TRAIN_URL = reverse("station-api:train-list")
PAGE_SIZE = TrainViewSet.pagination_class.page_size


def detail_url(train_id: int) -> str:
    return reverse("station-api:train-detail", args=[train_id])


class NotAuthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(TRAIN_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
