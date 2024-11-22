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
from station_api.schemas.examples.trains import (
    train_list_json,
    train_create_update_request_json,
    train_create_update_response_json,
    train_detail_json,
    train_upload_image_response_json,
    error_400_empty_fields,
    error_400_invalid_cargo_num_and_places_in_cargo,
    error_400_invalid_train_type,
    error_400_invalid_image_extension,
    error_400_invalid_image_size,
    error_404_not_found,
)
from station_api.serializers import (
    TrainReadSerializer,
    TrainCreateUpdateSerializer,
    TrainImageSerializer
)


train_request_example = OpenApiExample(
    name="Crew request example",
    value=train_create_update_request_json,
    request_only=True,
)

train_response_example = OpenApiExample(
    name="Crew response example",
    value=train_create_update_response_json,
    response_only=True,
)

train_image_response_example = OpenApiExample(
    name="Train upload image response example",
    value=train_upload_image_response_json,
    response_only=True,
)

empty_fields_example = OpenApiExample(
    name="Empty required fields example",
    value=error_400_empty_fields,
    response_only=True,
)

not_valid_cargo_num_and_places_in_cargo_example = OpenApiExample(
    name="Not valid cargo num and places in cargo",
    value=error_400_invalid_cargo_num_and_places_in_cargo,
    response_only=True,
)

not_valid_train_type = OpenApiExample(
    name="Not valid train type",
    value=error_400_invalid_train_type,
    response_only=True,
)

not_valid_image_extension = OpenApiExample(
    name="Not valid image extension example",
    value=error_400_invalid_image_extension,
    response_only=True,
)

not_valid_image_size = OpenApiExample(
    name="Not valid image size example",
    value=error_400_invalid_image_size,
    response_only=True,
)

not_found_response = OpenApiResponse(
    description="Not found",
    response=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            name="Not found",
            value=error_404_not_found,
            response_only=True,
        )
    ]
)

train_set_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of trains, allowing filter",
        parameters=[
            OpenApiParameter(
                name="train_type_name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by train_type_name or its part, case insensitive. "
                    "Example: '?train_type_name=fast'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="capacity_min",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by min capacity. The result: all the trains that "
                    "have capacity >= min_capacity. "
                    "Example: '?min_capacity=240'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="capacity_max",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by max capacity. The result: all the trains that "
                    "have capacity <= max_capacity. "
                    "Example: '?max_capacity=240'"
                ),
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                name="Train list example",
                value=train_list_json
            )
        ],
        responses={
            status.HTTP_200_OK: TrainReadSerializer(many=False),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response
        },
    ),
    create=extend_schema(
        description="Create a new train",
        request=TrainCreateUpdateSerializer(),
        examples=[
            train_request_example,
            train_response_example
        ],
        responses={
            status.HTTP_201_CREATED: TrainCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_cargo_num_and_places_in_cargo_example,
                    not_valid_train_type
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
        },
    ),
    retrieve=extend_schema(
        description="Retrieve detail train information",
        examples=[
            OpenApiExample(
                name="Train detail example",
                value=train_detail_json,
            )
        ],
        responses={
            status.HTTP_200_OK: TrainReadSerializer(),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        },
    ),
    update=extend_schema(
        description="Update train information",
        request=TrainCreateUpdateSerializer(),
        examples=[
            train_request_example,
            train_response_example
        ],
        responses={
            status.HTTP_200_OK: TrainCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_cargo_num_and_places_in_cargo_example,
                    not_valid_train_type
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    partial_update=extend_schema(
        description="Partial update train information",
        request=TrainCreateUpdateSerializer(partial=True),
        examples=[
            train_request_example,
            train_response_example
        ],
        responses={
            status.HTTP_200_OK: TrainCreateUpdateSerializer(partial=True),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    not_valid_cargo_num_and_places_in_cargo_example,
                    not_valid_train_type
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    destroy=extend_schema(
        description="Delete train",
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    upload_image=extend_schema(
        description="Upload image for a train. Up to 1 MB. "
                    "Allowed extensions: png, jpg, jpeg",
        request=TrainImageSerializer(),
        examples=[train_image_response_example],
        responses={
            status.HTTP_200_OK: TrainImageSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    not_valid_image_extension,
                    not_valid_image_size
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    )
)
