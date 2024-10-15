order_list_json = [
    {
        "id": 9,
        "tickets": [
            {
                "id": 17,
                "cargo": 6,
                "seat": 2,
                "trip": {
                    "id": 30,
                    "route": "Kyiv - Donetsk",
                    "train": "Train AB 012",
                    "train_type": "Night train",
                    "departure_time": "14 Oct 2024 13:00",
                    "arrival_time": "14 Oct 2024 18:00",
                    "train_capacity": 258
                }
            },
            {
                "id": 18,
                "cargo": 1,
                "seat": 3,
                "trip": {
                    "id": 31,
                    "route": "Rivne - Kyiv",
                    "train": "Bird AB 0323",
                    "train_type": "Super fast",
                    "departure_time": "15 Oct 2024 12:05",
                    "arrival_time": "15 Oct 2024 16:00",
                    "train_capacity": 120
                }
            }
        ],
        "created_at": "15 Oct 2024 12:56"
    },
    {
        "id": 5,
        "tickets": [
            {
                "id": 8,
                "cargo": 1,
                "seat": 1,
                "trip": {
                    "id": 32,
                    "route": "Rivne - Chernihiv",
                    "train": "Eagle 2024 AB",
                    "train_type": "Night train",
                    "departure_time": "13 Oct 2024 18:00",
                    "arrival_time": "13 Oct 2024 22:00",
                    "train_capacity": 75
                }
            },
            {
                "id": 9,
                "cargo": 1,
                "seat": 2,
                "trip": {
                    "id": 32,
                    "route": "Rivne - Chernihiv",
                    "train": "Eagle 2024 AB",
                    "train_type": "Night train",
                    "departure_time": "13 Oct 2024 18:00",
                    "arrival_time": "13 Oct 2024 22:00",
                    "train_capacity": 75
                }
            },
            {
                "id": 10,
                "cargo": 2,
                "seat": 4,
                "trip": {
                    "id": 32,
                    "route": "Rivne - Chernihiv",
                    "train": "Eagle 2024 AB",
                    "train_type": "Night train",
                    "departure_time": "13 Oct 2024 18:00",
                    "arrival_time": "13 Oct 2024 22:00",
                    "train_capacity": 75
                }
            }
        ],
        "created_at": "15 Oct 2024 12:21"
    }
]

order_create_request_json = {
    "tickets": [
        {
            "cargo": 1,
            "seat": 2,
            "trip": 33
        },
        {
            "cargo": 1,
            "seat": 3,
            "trip": 33
        }
    ]
}

order_create_response_json = {
    "id": 11,
    "tickets": [
        {
            "id": 20,
            "cargo": 1,
            "seat": 2,
            "trip": 33
        },
        {
            "id": 21,
            "cargo": 1,
            "seat": 3,
            "trip": 33
        }
    ],
    "created_at": "15 Oct 2024 13:13"
}

error_400_empty_fields = {
    "tickets": {
        "non_field_errors": [
            "This list may not be empty."
        ]
    }
}

error_400_invalid_place = {
    "tickets": [
        {
            "non_field_errors": [
                "The fields cargo, seat, trip must make a unique set."
            ]
        }
    ]
}
