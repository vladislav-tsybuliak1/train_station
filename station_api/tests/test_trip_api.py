from django.contrib.auth import get_user_model
from django.db.models import F, Count, QuerySet
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from station_api.models import (
    Station,
    Route,
    Train,
    Trip,
    TrainType,
    Order,
    Ticket, Crew
)
from station_api.serializers import TripListSerializer, TripRetrieveSerializer
from station_api.views import TripViewSet


TRIP_URL = reverse("station-api:trip-list")
PAGE_SIZE = TripViewSet.pagination_class.page_size


def detail_url(trip_id: int) -> str:
    return reverse("station-api:trip-detail", args=[trip_id])


def annotated_tickets_available(query: QuerySet) -> QuerySet:
    return query.annotate(
        tickets_available=(
            F("train__cargo_num")
            * F("train__places_in_cargo")
            - Count("tickets")
        )
    )


class NotAuthenticatedTripApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self) -> None:
        response = self.client.get(TRIP_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTripApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

        self.station_1 = Station.objects.create(
            name="Chernivtsi",
            latitude=48.29,
            longitude=25.39
        )
        self.station_2 = Station.objects.create(
            name="Donetsk",
            latitude=48.01,
            longitude=37.81
        )

        self.route_1 = Route.objects.create(
            source=self.station_1,
            destination=self.station_2,
            distance=950
        )
        self.route_2 = Route.objects.create(
            source=self.station_2,
            destination=self.station_1,
            distance=950
        )

        self.train_1 = Train.objects.create(
            name="Eagle-01",
            cargo_num=10,
            places_in_cargo=50,
            train_type=TrainType.objects.create(name="Inter-city")
        )
        self.train_2 = Train.objects.create(
            name="Eagle-02",
            cargo_num=10,
            places_in_cargo=10,
            train_type=TrainType.objects.create(name="Night-fast")
        )

        self.trip_1 = Trip.objects.create(
            route=self.route_1,
            train=self.train_1,
            departure_time="2024-01-01T12:00Z",
            arrival_time="2024-01-01T20:00Z"
        )
        self.trip_2 = Trip.objects.create(
            route=self.route_2,
            train=self.train_2,
            departure_time="2024-01-02T12:00Z",
            arrival_time="2024-01-02T20:00Z"
        )
        self.trip_3 = Trip.objects.create(
            route=self.route_1,
            train=self.train_2,
            departure_time="2024-01-03T12:00Z",
            arrival_time="2024-01-03T20:00Z"
        )
        self.trip_4 = Trip.objects.create(
            route=self.route_2,
            train=self.train_1,
            departure_time="2024-01-04T12:00Z",
            arrival_time="2024-01-04T20:00Z"
        )

        self.payload = {
            "route_id": self.route_1.id,
            "train_id": self.train_1.id,
            "departure_time": "2024-03-01T12:00:00Z",
            "arrival_time": "2024-03-01T14:00:00Z",
            "crew_ids": [],
        }

    def test_trip_list(self) -> None:
        response = self.client.get(TRIP_URL)
        trips = annotated_tickets_available(
            Trip.objects.order_by("departure_time")
        )[:PAGE_SIZE]
        serializer = TripListSerializer(trips, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_trip_filter_by_departure_date(self) -> None:
        departure_date = "2024-01-01"
        response = self.client.get(
            TRIP_URL,
            {"departure_date": departure_date}
        )
        trips = annotated_tickets_available(
            Trip.objects.filter(departure_time__date=departure_date)
            .order_by("departure_time")
        )[:PAGE_SIZE]
        serializer = TripListSerializer(trips, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_trip_filter_by_source_station(self) -> None:
        source_station = "chernivtsi"
        response = self.client.get(
            TRIP_URL,
            {"source_station": source_station}
        )
        trips = annotated_tickets_available(
            Trip.objects.filter(route__source__name__iexact=source_station).
            order_by("departure_time")
        )[:PAGE_SIZE]
        serializer = TripListSerializer(trips, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_trip_filter_by_destination_station(self) -> None:
        destination_station = "chernivtsi"
        response = self.client.get(
            TRIP_URL,
            {"destination_station": destination_station}
        )
        trips = annotated_tickets_available(
            Trip.objects.filter(
                route__destination__name__iexact=destination_station
            ).order_by("departure_time")
        )[:PAGE_SIZE]
        serializer = TripListSerializer(trips, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_trip_filter_by_train_type_name(self) -> None:
        train_type = "inter-city"
        response = self.client.get(
            TRIP_URL,
            {"train_type": train_type}
        )
        trips = annotated_tickets_available(
            Trip.objects.filter(
                train__train_type__name__icontains=train_type
            ).order_by("departure_time")
        )[:PAGE_SIZE]
        serializer = TripListSerializer(trips, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_trip_filter_by_tickets_available(self) -> None:
        trip = self.trip_1
        order = Order.objects.create(user=self.user)
        cargo = trip.train.cargo_num
        seat = trip.train.places_in_cargo
        [
            Ticket.objects.create(trip=trip, cargo=i, seat=j, order=order)
            for i in range(1, cargo + 1)
            for j in range(1, seat + 1)
        ]

        response = self.client.get(
            TRIP_URL,
            {"tickets_available": True}
        )
        trips = (
            annotated_tickets_available(Trip.objects.all())
            .filter(tickets_available__gt=0)
            .order_by("departure_time")
            [:PAGE_SIZE]
        )
        serializer = TripListSerializer(trips, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_trip_forbidden(self) -> None:
        response = self.client.post(TRIP_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_trip(self) -> None:
        order = Order.objects.create(user=self.user)
        trip = self.trip_1
        cargo = trip.train.cargo_num
        seat = trip.train.places_in_cargo
        [
            Ticket.objects.create(trip=trip, cargo=i, seat=j, order=order)
            for i in range(1, cargo // 2)
            for j in range(1, seat // 2)
        ]

        response = self.client.get(detail_url(trip.id))
        serializer = TripRetrieveSerializer(trip)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_trip_forbidden(self) -> None:
        response = self.client.put(detail_url(self.trip_1.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_trip_forbidden(self) -> None:
        response = self.client.patch(detail_url(self.trip_1.id), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_trip_forbidden(self) -> None:
        response = self.client.delete(detail_url(self.trip_1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminTripApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.station_1 = Station.objects.create(
            name="Chernivtsi",
            latitude=48.29,
            longitude=25.39
        )
        self.station_2 = Station.objects.create(
            name="Donetsk",
            latitude=48.01,
            longitude=37.81
        )

        self.route_1 = Route.objects.create(
            source=self.station_1,
            destination=self.station_2,
            distance=950
        )
        self.route_2 = Route.objects.create(
            source=self.station_2,
            destination=self.station_1,
            distance=950
        )

        self.train = Train.objects.create(
            name="Eagle-01",
            cargo_num=10,
            places_in_cargo=50,
            train_type=TrainType.objects.create(name="Inter-city")
        )

        self.trip = Trip.objects.create(
            route=self.route_1,
            train=self.train,
            departure_time="2024-01-01T12:00:00Z",
            arrival_time="2024-01-01T20:00:00Z"
        )

        self.crew_1 = Crew.objects.create(first_name="John", last_name="Doe")
        self.crew_2 = Crew.objects.create(first_name="Johny", last_name="Don")

        self.payload = {
            "route_id": self.route_2.id,
            "train_id": self.train.id,
            "departure_time": "2024-03-01 12:00",
            "arrival_time": "2024-03-01 14:00",
            "crew_ids": [self.crew_1.id, self.crew_2.id]
        }


    def test_create_trip(self) -> None:
        response = self.client.post(TRIP_URL, self.payload)
        trip = Trip.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.payload["route_id"], trip.route.id)
        self.assertEqual(self.payload["train_id"], trip.train.id)
        self.assertEqual(
            self.payload["departure_time"],
            trip.departure_time.strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(
            self.payload["arrival_time"],
            trip.arrival_time.strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(
            self.payload["crew_ids"],
            list(trip.crew.values_list("id", flat=True))
        )

    def test_create_trip_invalid_times(self) -> None:
        self.payload["arrival_time"] = "2024-01-01T10:00:00Z"
        self.payload["departure_time"] = "2024-01-01T11:00:00Z"
        response = self.client.post(TRIP_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_trip(self) -> None:
        trip = self.trip
        response = self.client.put(detail_url(trip.id), self.payload)
        trip.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payload["route_id"], trip.route.id)
        self.assertEqual(
            self.payload["departure_time"],
            trip.departure_time.strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(
            self.payload["arrival_time"],
            trip.arrival_time.strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(
            self.payload["crew_ids"],
            list(trip.crew.values_list("id", flat=True))
        )

    def test_delete_trip(self) -> None:
        trip = self.trip
        response = self.client.delete(detail_url(trip.id))
        trip_exists = Trip.objects.filter(id=trip.id).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(trip_exists)
