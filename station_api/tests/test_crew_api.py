from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import Crew
from station_api.serializers import CrewReadSerializer
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


class AuthenticatedCrewApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

        Crew.objects.create(first_name="John", last_name="Doe")
        Crew.objects.create(first_name="Jane", last_name="Doe")
        Crew.objects.create(first_name="Rick", last_name="Astley")

        self.payload = {
            "first_name": "Test",
            "last_name": "Test"
        }

    def test_crew_list(self) -> None:
        response = self.client.get(CREW_URL)
        crews = Crew.objects.all()[:PAGE_SIZE]
        serializer = CrewReadSerializer(crews, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_crew_by_full_name(self) -> None:
        name_to_search = "j doe"
        response = self.client.get(CREW_URL, {"full_name": name_to_search})
        crews = Crew.objects.filter(
            first_name__icontains=name_to_search.split(" ")[0],
            last_name__icontains=name_to_search.split(" ")[1],
        )[:PAGE_SIZE]
        serializer = CrewReadSerializer(crews, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_crew_forbidden(self) -> None:
        response = self.client.post(CREW_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_crew(self) -> None:
        response = self.client.get(detail_url(1))
        serializer = CrewReadSerializer(Crew.objects.get(pk=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_crew_forbidden(self) -> None:
        response = self.client.put(detail_url(1), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_crew_forbidden(self) -> None:
        response = self.client.patch(detail_url(1), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_crew_forbidden(self) -> None:
        response = self.client.delete(detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
