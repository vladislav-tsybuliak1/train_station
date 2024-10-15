train_type_list_json = [
    {
        "id": 1,
        "name": "Night train"
    },
    {
        "id": 2,
        "name": "Super fast"
    },
    {
        "id": 3,
        "name": "Inter-city"
    },
    {
        "id": 4,
        "name": "Regional"
    }
]

train_type_create_request_json = {
    "name": "Regional"
}

train_type_create_response_json = {
    "id": 4,
    "name": "Regional"
}

error_400_empty_fields = {
    "name": [
        "This field is required."
    ]
}

error_400_name_already_exists = {
    "name": [
        "train type with this name already exists."
    ]
}
