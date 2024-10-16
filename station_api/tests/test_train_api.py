import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.db.models import ExpressionWrapper, F, IntegerField
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import Train, TrainType
from station_api.serializers import TrainReadSerializer
from station_api.views import TrainViewSet


TRAIN_URL = reverse("station-api:train-list")
PAGE_SIZE = TrainViewSet.pagination_class.page_size


def detail_url(train_id: int) -> str:
    return reverse("station-api:train-detail", args=[train_id])


def image_upload_url(train_id: int) -> str:
    return reverse("station-api:train-upload-image", args=[train_id])


class NotAuthenticatedTrainApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(TRAIN_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

        self.train_type_1 = TrainType.objects.create(name="Inter-city")
        self.train_type_2 = TrainType.objects.create(name="Night-fast")

        self.train_1 = Train.objects.create(
            name="Eagle-01",
            cargo_num=10,
            places_in_cargo=50,
            train_type=self.train_type_1
        )
        Train.objects.create(
            name="Eagle-02",
            cargo_num=10,
            places_in_cargo=10,
            train_type=self.train_type_1
        )
        Train.objects.create(
            name="Tiger-01",
            cargo_num=10,
            places_in_cargo=50,
            train_type=self.train_type_2
        )
        Train.objects.create(
            name="Tiger-02",
            cargo_num=10,
            places_in_cargo=10,
            train_type=self.train_type_2
        )

        self.payload = {
            "name": "Tiger-03",
            "cargo_num": 10,
            "places_in_cargo": 10,
            "train_type": self.train_type_2.id
        }

    def test_train_list(self) -> None:
        response = self.client.get(TRAIN_URL)
        trains = Train.objects.all()[:PAGE_SIZE]
        serializer = TrainReadSerializer(trains, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_train_by_train_type_name(self) -> None:
        name_to_search = self.train_type_1.name
        response = self.client.get(
            TRAIN_URL,
            {"train_type_name": name_to_search}
        )
        trains = (
            Train.objects.filter(
                train_type__name__contains=name_to_search
            )[:PAGE_SIZE]
        )
        serializer = TrainReadSerializer(trains, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_train_by_min_capacity(self) -> None:
        capacity_min = 200
        response = self.client.get(
            TRAIN_URL,
            {"capacity_min": capacity_min}
        )
        trains = (
            Train.objects.annotate(
                annotated_capacity=ExpressionWrapper(
                    F("cargo_num") * F("places_in_cargo"),
                    output_field=IntegerField()
                )
            ).filter(annotated_capacity__gte=capacity_min)[:PAGE_SIZE]
        )
        serializer = TrainReadSerializer(trains, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_train_by_max_capacity(self) -> None:
        capacity_max = 200
        response = self.client.get(
            TRAIN_URL,
            {"capacity_min": capacity_max}
        )
        trains = (
            Train.objects.annotate(
                annotated_capacity=ExpressionWrapper(
                    F("cargo_num") * F("places_in_cargo"),
                    output_field=IntegerField()
                )
            ).filter(annotated_capacity__gte=capacity_max)[:PAGE_SIZE]
        )
        serializer = TrainReadSerializer(trains, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_train_forbidden(self) -> None:
        response = self.client.post(TRAIN_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_train(self) -> None:
        train = self.train_1
        response = self.client.get(detail_url(train.id))
        serializer = TrainReadSerializer(train)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_train_forbidden(self) -> None:
        response = self.client.put(detail_url(self.train_1.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_train_forbidden(self) -> None:
        response = self.client.patch(detail_url(self.train_1.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_train_forbidden(self) -> None:
        response = self.client.delete(detail_url(self.train_1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_image_to_train_forbidden(self) -> None:
        url = image_upload_url(self.train_1.id)
        response = self.client.post(
            url,
            {"train_image": "some_possible_image"},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
