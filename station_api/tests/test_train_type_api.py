from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import TrainType
from station_api.serializers import TrainTypeSerializer
from station_api.views import TrainTypeViewSet


TRAIN_TYPE_URL = reverse("station-api:traintype-list")
PAGE_SIZE = TrainTypeViewSet.pagination_class.page_size


class NotAuthenticatedTrainTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(TRAIN_TYPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

        self.payload = {
            "name": "Test"
        }

        TrainType.objects.create(name="Night")
        TrainType.objects.create(name="Night-fast")
        TrainType.objects.create(name="Inter-city")
        TrainType.objects.create(name="Regional")

    def test_train_type_list(self) -> None:
        response = self.client.get(TRAIN_TYPE_URL)
        train_types = TrainType.objects.all()[:PAGE_SIZE]
        serializer = TrainTypeSerializer(train_types, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_train_type_filter_by_name(self) -> None:
        name_to_search = "night"
        response = self.client.get(TRAIN_TYPE_URL, {"name": name_to_search})
        train_types = (
            TrainType.objects.filter(
                name__icontains=name_to_search
            )[:PAGE_SIZE]
        )
        serializer = TrainTypeSerializer(train_types, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_train_type_forbidden(self) -> None:
        response = self.client.post(TRAIN_TYPE_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
