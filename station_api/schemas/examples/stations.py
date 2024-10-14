station_list_json = {
    "pages": 2,
    "count": 7,
    "next": "http://localhost:8000/api/v1/train-station/stations/?page=2",
    "previous": None,
    "results": [
        {
            "id": 3,
            "name": "Chernihiv",
            "latitude": 51.5,
            "longitude": 31.32
        },
        {
            "id": 4,
            "name": "Chernivtsi",
            "latitude": 48.29,
            "longitude": 25.39
        },
        {
            "id": 7,
            "name": "Donetsk",
            "latitude": 48.01,
            "longitude": 37.81
        },
        {
            "id": 1,
            "name": "Kyiv",
            "latitude": 50.45,
            "longitude": 30.52
        },
        {
            "id": 2,
            "name": "Lviv",
            "latitude": 49.85,
            "longitude": 24.03
        }
    ]
}

station_create_request_json = {
    "name": "Lutsk",
    "latitude": 50.76,
    "longitude": 25.34
}

station_create_response_json = {
    "id": 8,
    "name": "Lutsk",
    "latitude": 50.76,
    "longitude": 25.34
}

error_400_empty_fields = {
    "name": [
        "This field is required."
    ],
    "latitude": [
        "This field is required."
    ],
    "longitude": [
        "This field is required."
    ]
}

error_400_same_station_name = {
    "name": [
        "station with this name already exists."
    ]
}

error_400_not_valid_latitude_and_longitude = {
    "latitude": [
        "Latitude must be between -90 and 90 degrees."
    ],
    "longitude": [
        "Longitude must be between -180 and 180 degrees."
    ]
}
