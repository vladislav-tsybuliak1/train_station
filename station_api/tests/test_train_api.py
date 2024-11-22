import os
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


class AdminTrainApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.train_type_1 = TrainType.objects.create(name="Inter-city")
        self.train_type_2 = TrainType.objects.create(name="Night")

        self.train = Train.objects.create(
            name="Tiger-01",
            cargo_num=10,
            places_in_cargo=50,
            train_type=self.train_type_1
        )

        self.payload = {
            "name": "Tiger-02",
            "cargo_num": 5,
            "places_in_cargo": 45,
            "train_type": self.train_type_2.id
        }

    def test_create_train(self) -> None:
        response = self.client.post(TRAIN_URL, self.payload)
        train = Train.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.payload["name"], train.name)
        self.assertEqual(self.payload["cargo_num"], train.cargo_num)
        self.assertEqual(
            self.payload["places_in_cargo"],
            train.places_in_cargo
        )
        self.assertEqual(
            self.payload["train_type"],
            train.train_type.id
        )

    def test_create_train_negative_cargo_and_places_in_cargo(self) -> None:
        self.payload["cargo_num"] = -10
        self.payload["places_in_cargo"] = -10
        response = self.client.post(TRAIN_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_train(self) -> None:
        train = self.train
        response = self.client.put(detail_url(train.id), self.payload)
        train.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payload["name"], train.name)
        self.assertEqual(self.payload["cargo_num"], train.cargo_num)
        self.assertEqual(
            self.payload["places_in_cargo"],
            train.places_in_cargo
        )
        self.assertEqual(
            self.payload["train_type"],
            train.train_type.id
        )

    def test_partial_update_train(self) -> None:
        train = self.train
        self.payload.pop("train_type")
        self.payload.pop("places_in_cargo")
        response = self.client.patch(detail_url(train.id), self.payload)
        train.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payload["name"], train.name)
        self.assertEqual(self.payload["cargo_num"], train.cargo_num)

    def test_delete_route(self) -> None:
        train = self.train
        response = self.client.delete(detail_url(train.id))
        train_exists = Train.objects.filter(id=train.id).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(train_exists)

    def test_upload_image_to_train(self) -> None:
        train = self.train
        url = image_upload_url(train.id)
        with tempfile.NamedTemporaryFile(suffix=".png") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="PNG")
            ntf.seek(0)
            response = self.client.post(
                url,
                {"train_image": ntf},
                format="multipart"
            )
        train.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(os.path.exists(train.train_image.path))

        train.train_image.delete()

    def test_upload_not_valid_size_image_to_train(self) -> None:
        train = self.train
        url = image_upload_url(train.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10000, 10000))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            response = self.client.post(
                url,
                {"train_image": ntf},
                format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_not_valid_extension_image_to_train(self) -> None:
        train = self.train
        url = image_upload_url(train.id)
        with tempfile.NamedTemporaryFile(suffix=".gif") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="GIF")
            ntf.seek(0)
            response = self.client.post(
                url,
                {"train_image": ntf},
                format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
