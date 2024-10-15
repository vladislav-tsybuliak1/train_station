from drf_spectacular.utils import OpenApiExample

register_request_example = OpenApiExample(
    name="User register request example",
    value={
        "email": "example_email@test.com",
        "password": "test123test"
    },
    request_only=True,
)

register_response_example = OpenApiExample(
    name="User register response example",
    value={
        "id": 5,
        "email": "example_email@test.com",
        "is_staff": False
    },
    response_only=True
)

empty_fields_example = OpenApiExample(
    name="Empty required fields example",
    value={
        "email": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ]
    },
    response_only=True,
)

not_valid_email_example = OpenApiExample(
    name="Not valid email example",
    value={
        "email": [
            "Enter a valid email address."
        ]
    },
    response_only=True,
)

not_valid_password_example = OpenApiExample(
    name="Not valid password example",
    value={
        "password": [
            "Ensure this field has at least 5 characters."
        ]
    },
    response_only=True,
)

email_already_exists_example = OpenApiExample(
    name="User with this email already exists example",
    value={
        "email": [
            "user with this email address already exists."
        ]
    },
    response_only=True,
)
