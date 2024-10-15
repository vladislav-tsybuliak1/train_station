from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.views import CrewViewSet


CREW_URL = reverse("station-api:crew-list")
PAGE_SIZE = CrewViewSet.pagination_class.page_size


def detail_url(crew_id: int) -> str:
    return reverse("station-api:crew-detail", args=[crew_id])


class NotAuthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
