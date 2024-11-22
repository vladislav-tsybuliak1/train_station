from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)
from rest_framework import status

from station_api.schemas.examples.common_responses import (
    unauthorized_response,
    forbidden_response,
)
from station_api.schemas.examples.train_types import (
    train_type_list_json,
    train_type_create_request_json,
    train_type_create_response_json,
    error_400_empty_fields,
    error_400_name_already_exists
)
from station_api.serializers import TrainTypeSerializer


train_type_list_create_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of train types, allowing filter",
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by train type name or its part, case insensitive. "
                    "Example: '?name=fast'"
                ),
                required=False,
            )
        ],
        examples=[
            OpenApiExample(
                name="Train type list example",
                value=train_type_list_json,
            )
        ],
        responses={
            status.HTTP_200_OK: TrainTypeSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response
        },
    ),
    create=extend_schema(
        description="Create a new train type",
        request=TrainTypeSerializer(),
        examples=[
            OpenApiExample(
                name="Train type request example",
                value=train_type_create_request_json,
                request_only=True,
            ),
            OpenApiExample(
                name="Train type response example",
                value=train_type_create_response_json,
                response_only=True,
            )
        ],
        responses={
            status.HTTP_201_CREATED: TrainTypeSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="Empty required fields example",
                        value=error_400_empty_fields,
                        response_only=True,
                    ),
                    OpenApiExample(
                        name="Not unique train type name example",
                        value=error_400_name_already_exists,
                        response_only=True,
                    )
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
        }
    )
)
