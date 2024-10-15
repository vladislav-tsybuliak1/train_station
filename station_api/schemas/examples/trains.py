train_list_json = [
    {
        "id": 1,
        "name": "Owl 1213",
        "cargo_num": 3,
        "places_in_cargo": 20,
        "capacity": 60,
        "train_type": "Night train",
        "train_image": "http://localhost:8000/media/uploads/trains/"
                       "new-2ee2e586-0467-42a7-862e-df53515c62fe.png"
    },
    {
        "id": 2,
        "name": "Train AB 012",
        "cargo_num": 6,
        "places_in_cargo": 43,
        "capacity": 258,
        "train_type": "Night train",
        "train_image": None
    },
    {
        "id": 3,
        "name": "Freedom 2133",
        "cargo_num": 4,
        "places_in_cargo": 10,
        "capacity": 40,
        "train_type": "Inter-city",
        "train_image": "http://localhost:8000/media/uploads/trains/"
                       "freedom-2133-aea03a10-d019-4e4a-8c72-49b7f0b2edd1.png"
    },
    {
        "id": 4,
        "name": "Owl 1212",
        "cargo_num": 4,
        "places_in_cargo": 40,
        "capacity": 160,
        "train_type": "Night train",
        "train_image": "http://localhost:8000/media/uploads/trains/"
                       "owl-1212-6ecb3eef-8031-4947-9f5a-f734eb9dc880.png"
    },
    {
        "id": 5,
        "name": "Eagle AS 0323",
        "cargo_num": 5,
        "places_in_cargo": 43,
        "capacity": 215,
        "train_type": "Regional",
        "train_image": "http://localhost:8000/media/uploads/trains/"
                       "eagle-as-0322-932ceb26-df58-41b6-9b04-59f08caa24cd.png"
    }
]

train_detail_json = {
    "id": 1,
    "name": "Owl 1213",
    "cargo_num": 3,
    "places_in_cargo": 20,
    "capacity": 60,
    "train_type": "Night train",
    "train_image": "http://localhost:8000/media/uploads/trains/"
                   "new-2ee2e586-0467-42a7-862e-df53515c62fe.png"
}

train_create_update_request_json = {
    "name": "Eagle 2024 AB",
    "cargo_num": 5,
    "places_in_cargo": 15,
    "train_type": 1
}

train_upload_image_response_json = {
    "id": 1,
    "train_image": "http://localhost:8000/media/uploads/trains/"
                   "new-2ee2e586-0467-42a7-862e-df53515c62fe.png"
}

train_create_update_response_json = {
    "id": 11,
    "name": "Eagle 2024 AB",
    "cargo_num": 5,
    "places_in_cargo": 15,
    "train_type": 1
}

error_400_empty_fields = {
    "name": [
        "This field is required."
    ],
    "cargo_num": [
        "This field is required."
    ],
    "places_in_cargo": [
        "This field is required."
    ],
    "train_type": [
        "This field is required."
    ]
}

error_400_invalid_cargo_num_and_places_in_cargo = {
    "cargo_num": [
        "Ensure this value is greater than or equal to 0."
    ],
    "places_in_cargo": [
        "Ensure this value is greater than or equal to 0."
    ]
}

error_400_invalid_train_type = {
    "train_type": [
        "Invalid pk \"122\" - object does not exist."
    ]
}

error_404_not_found = {
    "detail": "No Train matches the given query."
}

error_400_invalid_image_extension = {
    "train_image": [
        "Upload a valid image. "
        "The file you uploaded was either not an image or a corrupted image."
    ]
}

error_400_invalid_image_size = {
    "train_image": [
        "The image size should be less than 1 MB"
    ]
}
