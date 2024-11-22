route_list_json = [
    {
        "id": 1,
        "source": "Chernivtsi",
        "destination": "Chernihiv",
        "distance": 332.0
    },
    {
        "id": 2,
        "source": "Chernihiv",
        "destination": "Kyiv",
        "distance": 332.0
    },
    {
        "id": 3,
        "source": "Kyiv",
        "destination": "Chernivtsi",
        "distance": 550.0
    },
    {
        "id": 4,
        "source": "Lviv",
        "destination": "Chernivtsi",
        "distance": 750.0
    },
    {
        "id": 5,
        "source": "Chernivtsi",
        "destination": "Kyiv",
        "distance": 750.0
    }
]

route_create_update_request_json = {
    "source": 1,
    "destination": 7,
    "distance": 390
}

route_create_update_response_json = {
    "id": 9,
    "source": 1,
    "destination": 7,
    "distance": 390.0
}

route_detail_json = {
    "id": 1,
    "source": "Chernivtsi",
    "destination": "Chernihiv",
    "distance": 332.0
}

error_400_empty_fields = {
    "source": [
        "This field is required."
    ],
    "destination": [
        "This field is required."
    ],
    "distance": [
        "This field is required."
    ]
}

error_400_not_valid_distance = {
    "distance": [
        "Ensure this value is greater than or equal to 0."
    ]
}

error_400_same_source_destination = {
    "non_field_errors": [
        "The source and destination stations must be different."
    ]
}

error_400_invalid_source_destination = {
    "source": [
        "Invalid pk \"9\" - object does not exist."
    ],
    "destination": [
        "Invalid pk \"12\" - object does not exist."
    ]
}

error_404_not_found = {
    "detail": "No Route matches the given query."
}
