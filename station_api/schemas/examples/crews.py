crew_list_json = [
    {
        "id": 7,
        "full_name": "Andrew Kotsyi",
        "crew_image": None
    },
    {
        "id": 8,
        "full_name": "Bohdan Hmel",
        "crew_image": None
    },
    {
        "id": 6,
        "full_name": "Johny Depp",
        "crew_image": None
    },
    {
        "id": 1,
        "full_name": "Johny Doe",
        "crew_image": "http://localhost:8000/media/uploads/crew/"
                      "johny-doe-c0b937a9-d9a2-40c5-882c-03b01cf0a214.png"
    },
    {
        "id": 2,
        "full_name": "Rick Astley",
        "crew_image": None
    }
]

crew_detail_json = {
    "id": 1,
    "full_name": "Johny Doe",
    "crew_image": "http://localhost:8000/media/uploads/crew/"
                  "johny-doe-c0b937a9-d9a2-40c5-882c-03b01cf0a214.png"
}

crew_create_update_request_json = {
    "first_name": "Bohdan",
    "last_name": "Hmel"
}

crew_create_update_response_json = {
    "id": 8,
    "first_name": "Bohdan",
    "last_name": "Hmel"
}

crew_upload_image_response_json = {
    "id": 2,
    "crew_image": "http://localhost:8000/media/uploads/crew/"
                  "rick-astley-aec99aa5-0fa2-45d0-ad88-10a23ff07994.png"
}

error_400_empty_fields = {
    "first_name": [
        "This field is required."
    ],
    "last_name": [
        "This field is required."
    ]
}

error_400_invalid_names = {
    "first_name": [
        "Bohdan?1 contains non-english letters"
    ],
    "last_name": [
        "Hmel-1 contains non-english letters"
    ]
}

error_404_not_found = {
    "detail": "No Crew matches the given query."
}

error_400_invalid_image_extension = {
    "crew_image": [
        "Upload a valid image. "
        "The file you uploaded was either not an image or a corrupted image."
    ]
}

error_400_invalid_image_size = {
    "crew_image": [
        "The image size should be less than 1 MB"
    ]
}
