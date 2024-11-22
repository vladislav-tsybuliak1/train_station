from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse
)

from user_api.schemas.examples.users import (
    register_request_example,
    register_response_example,
    empty_fields_example,
    not_valid_password_example,
    not_valid_email_example,
    email_already_exists_example,
    user_detail_example, forbidden_example
)
from user_api.serializers import UserSerializer


user_register_schema = extend_schema_view(
    post=extend_schema(
        description="Register new user",
        request=UserSerializer(),
        examples=[
            register_request_example,
            register_response_example
        ],
        responses={
            201: UserSerializer(),
            400: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_email_example,
                    not_valid_password_example,
                    email_already_exists_example
                ]
            )
        }
    )
)

user_manage_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve information about yourself",
        examples=[user_detail_example],
        responses={
            200: UserSerializer(),
            403: OpenApiResponse(
                description="Forbidden",
                response=OpenApiTypes.OBJECT,
                examples=[forbidden_example]
            )
        }
    ),
    put=extend_schema(
        description="Update email and password",
        request=UserSerializer(),
        examples=[
            register_request_example,
            register_response_example
        ],
        responses={
            200: UserSerializer(),
            400: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_email_example,
                    not_valid_password_example,
                    email_already_exists_example
                ]
            ),
            403: OpenApiResponse(
                description="Forbidden",
                response=OpenApiTypes.OBJECT,
                examples=[forbidden_example]
            )
        }
    ),
    patch=extend_schema(
        description="Update email or password",
        request=UserSerializer(partial=True),
        examples=[
            register_request_example,
            register_response_example
        ],
        responses={
            200: UserSerializer(),
            400: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    not_valid_email_example,
                    not_valid_password_example,
                    email_already_exists_example
                ]
            ),
            403: OpenApiResponse(
                description="Forbidden",
                response=OpenApiTypes.OBJECT,
                examples=[forbidden_example]
            )
        }
    )
)
