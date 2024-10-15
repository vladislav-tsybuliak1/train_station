trip_list_json = [
    {
        "id": 30,
        "route": "Kyiv - Donetsk",
        "train": "Train AB 012",
        "train_type": "Night train",
        "departure_time": "14 Oct 2024 13:00",
        "arrival_time": "14 Oct 2024 18:00",
        "train_capacity": 258,
        "tickets_available": 255
    },
    {
        "id": 31,
        "route": "Rivne - Kyiv",
        "train": "Bird AB 0323",
        "train_type": "Super fast",
        "departure_time": "15 Oct 2024 12:05",
        "arrival_time": "15 Oct 2024 16:00",
        "train_capacity": 120,
        "tickets_available": 120
    },
    {
        "id": 33,
        "route": "Chernivtsi - Kyiv",
        "train": "Bird AB 0323",
        "train_type": "Super fast",
        "departure_time": "14 Oct 2024 00:00",
        "arrival_time": "14 Oct 2024 10:00",
        "train_capacity": 120,
        "tickets_available": 120
    },
    {
        "id": 32,
        "route": "Rivne - Chernihiv",
        "train": "Eagle 2024 AB",
        "train_type": "Night train",
        "departure_time": "13 Oct 2024 18:00",
        "arrival_time": "13 Oct 2024 22:00",
        "train_capacity": 75,
        "tickets_available": 70
    },
    {
        "id": 34,
        "route": "Rivne - Lviv",
        "train": "Eagle 2024 AB",
        "train_type": "Night train",
        "departure_time": "15 Oct 2024 12:00",
        "arrival_time": "15 Oct 2024 18:00",
        "train_capacity": 150,
        "tickets_available": 149
    }
]

trip_create_update_request_json = {
    "route_id": 4,
    "train_id": 8,
    "departure_time": "2024-10-11 12:00",
    "arrival_time": "2024-10-11 19:27",
    "crew_ids": [1, 2]
}

trip_create_update_response_json = {
    "id": 35,
    "route": "Lviv - Chernivtsi",
    "train": "Eagle AS 0322",
    "departure_time": "2024-10-11T12:00:00Z",
    "arrival_time": "2024-10-11T19:27:00Z",
    "crew": [
        1,
        2
    ]
}

trip_detail_json = {
    "id": 30,
    "route": {
        "id": 9,
        "source": "Kyiv",
        "destination": "Donetsk",
        "distance": 390.0
    },
    "train": {
        "id": 2,
        "name": "Train AB 012",
        "cargo_num": 6,
        "places_in_cargo": 43,
        "capacity": 258,
        "train_type": "Night train",
        "train_image": None
    },
    "departure_time": "14 Oct 2024 13:00",
    "arrival_time": "14 Oct 2024 18:00",
    "crew": [
        "Johny Doe",
        "Rick Astley"
    ],
    "taken_places": [
        {
            "cargo": 1,
            "seat": 3
        },
        {
            "cargo": 2,
            "seat": 4
        },
        {
            "cargo": 2,
            "seat": 5
        }
    ]
}

error_400_empty_fields = {
    "route_id": [
        "This field is required."
    ],
    "train_id": [
        "This field is required."
    ],
    "departure_time": [
        "This field is required."
    ],
    "arrival_time": [
        "This field is required."
    ],
    "crew_ids": [
        "This field is required."
    ]
}

error_400_invalid_route = {
    "detail": "No Route matches the given query."
}

error_400_invalid_train = {
    "detail": "No Train matches the given query."
}

error_400_invalid_crew = {
    "detail": "No Crew matches the given query."
}

error_400_arrival_time_before_departure_time = {
    "non_field_errors": [
        "Departure time must be before arrival time."
    ]
}

error_404_not_found = {
    "detail": "No Trip matches the given query."
}
