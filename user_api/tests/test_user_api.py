from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


CREATE_USER_URL = reverse("user-api:create")
MANAGE_USER_URL = reverse("user-api:manage")


class PublicUserApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            "email": "test@test.com",
            "password": "test123test",
        }

    def test_create_user_success(self) -> None:
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.payload["email"])
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertNotIn("password", response.data)

    def test_create_user_password_too_short(self) -> None:
        self.payload["password"] = "12"
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.payload["email"]
        ).exists()
        self.assertFalse(user_exists)


class PrivateUserApiTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="testpass123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.payload = {
            "email": "newemail@test.com",
            "password": "newpass123",
        }

    def test_retrieve_user_info(self) -> None:
        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertNotIn("password", response.data)

    def test_update_user_info(self) -> None:
        response = self.client.patch(MANAGE_USER_URL, self.payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, self.payload["email"])
        self.assertTrue(
            self.user.check_password(self.payload["password"])
        )

    def test_partial_update_user_info(self) -> None:
        self.payload.pop("password")

        response = self.client.patch(MANAGE_USER_URL, self.payload)
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, self.payload["email"])
        self.assertTrue(self.user.check_password("testpass123"))

    def test_unauthorized_user_cannot_access_profile(self) -> None:
        self.client.force_authenticate(user=None)
        response = self.client.get(MANAGE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
