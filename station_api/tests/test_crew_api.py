import os
import tempfile

from PIL import Image
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


def image_upload_url(crew_id: int) -> str:
    return reverse("station-api:crew-upload-image", args=[crew_id])


class NotAuthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
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

    def test_upload_image_to_crew_forbidden(self) -> None:
        url = image_upload_url(1)
        response = self.client.post(
            url,
            {"crew_image": "some_possible_image"},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.crew = Crew.objects.create(
            first_name="John",
            last_name="Doe"
        )

        self.payload = {
            "first_name": "Test",
            "last_name": "Test"
        }

    def test_create_crew(self) -> None:
        response = self.client.post(CREW_URL, self.payload)
        crew = Crew.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.payload["first_name"], crew.first_name)
        self.assertEqual(self.payload["last_name"], crew.last_name)

    def test_create_crew_with_invalid_name(self) -> None:
        self.payload["first_name"] = "With12numbers"
        response = self.client.post(CREW_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_crew(self) -> None:
        crew = self.crew
        response = self.client.put(detail_url(crew.id), self.payload)
        crew.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payload["first_name"], crew.first_name)
        self.assertEqual(self.payload["last_name"], crew.last_name)

    def test_partial_update_crew(self) -> None:
        crew = self.crew
        payload = {"first_name": "Test"}
        response = self.client.patch(detail_url(crew.id), payload)
        crew.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["first_name"], crew.first_name)

    def test_delete_crew(self) -> None:
        crew = self.crew
        response = self.client.delete(detail_url(crew.id))
        crew_exists = Crew.objects.filter(id=crew.id).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(crew_exists)

    def test_upload_image_to_crew(self) -> None:
        crew = self.crew
        url = image_upload_url(crew.id)
        with tempfile.NamedTemporaryFile(suffix=".png") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="PNG")
            ntf.seek(0)
            response = self.client.post(
                url,
                {"crew_image": ntf},
                format="multipart"
            )
        crew.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(os.path.exists(crew.crew_image.path))

        crew.crew_image.delete()

    def test_upload_not_valid_size_image_to_crew(self) -> None:
        crew = self.crew
        url = image_upload_url(crew.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10000, 10000))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            response = self.client.post(
                url,
                {"crew_image": ntf},
                format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_not_valid_extension_image_to_crew(self) -> None:
        crew = self.crew
        url = image_upload_url(crew.id)
        with tempfile.NamedTemporaryFile(suffix=".gif") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="GIF")
            ntf.seek(0)
            response = self.client.post(
                url,
                {"crew_image": ntf},
                format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
