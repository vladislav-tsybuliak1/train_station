from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import Order, Ticket, Trip, Train, Route, Station, \
    TrainType
from station_api.serializers import OrderListSerializer
from station_api.views import OrderViewSet

ORDER_URL = reverse("station-api:order-list")
PAGE_SIZE = OrderViewSet.pagination_class.page_size


class NotAuthenticatedOrderApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

        self.station_1 = Station.objects.create(
            name="Kyiv",
            latitude=50.45,
            longitude=30.52
        )
        self.station_2 = Station.objects.create(
            name="Lviv",
            latitude=49.84,
            longitude=24.02
        )

        self.route = Route.objects.create(
            source=self.station_1,
            destination=self.station_2,
            distance=550
        )

        self.train = Train.objects.create(
            name="Intercity Express",
            cargo_num=3,
            places_in_cargo=50,
            train_type=TrainType.objects.create(name="Inter-city")
        )

        self.trip = Trip.objects.create(
            route=self.route,
            train=self.train,
            departure_time="2024-01-01T08:00:00Z",
            arrival_time="2024-01-01T12:00:00Z"
        )

        self.payload = {
            "tickets": [
                {
                    "cargo": 1,
                    "seat": 1,
                    "trip": self.trip.id
                },
                {
                    "cargo": 1,
                    "seat": 2,
                    "trip": self.trip.id
                }
            ]
        }

    def test_list_orders(self) -> None:
        Order.objects.create(user=self.user)

        response = self.client.get(ORDER_URL)
        orders = Order.objects.filter(user=self.user)[:PAGE_SIZE]
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_order(self) -> None:
        response = self.client.post(ORDER_URL, self.payload, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=response.data["id"])
        tickets = Ticket.objects.filter(order=order)

        self.assertEqual(tickets.count(), 2)
        for ticket, ticket_data in zip(tickets, self.payload["tickets"]):
            self.assertEqual(ticket.cargo, ticket_data["cargo"])
            self.assertEqual(ticket.seat, ticket_data["seat"])
            self.assertEqual(ticket.trip.id, ticket_data["trip"])

    def test_create_order_invalid_ticket(self) -> None:
        self.payload["tickets"][0]["seat"] = 100
        response = self.client.post(ORDER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
