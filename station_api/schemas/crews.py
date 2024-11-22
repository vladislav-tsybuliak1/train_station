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
from station_api.schemas.examples.crews import (
    crew_list_json,
    crew_create_update_request_json,
    crew_create_update_response_json,
    crew_detail_json,
    crew_upload_image_response_json,
    error_400_empty_fields,
    error_400_invalid_names,
    error_404_not_found,
    error_400_invalid_image_extension,
    error_400_invalid_image_size,
)
from station_api.serializers import (
    CrewReadSerializer,
    CrewCreateUpdateSerializer,
    CrewImageSerializer
)


crew_request_example = OpenApiExample(
    name="Crew request example",
    value=crew_create_update_request_json,
    request_only=True,
)

crew_response_example = OpenApiExample(
    name="Crew response example",
    value=crew_create_update_response_json,
    response_only=True,
)

crew_image_response_example = OpenApiExample(
    name="Crew upload image response example",
    value=crew_upload_image_response_json,
    response_only=True,
)

empty_fields_example = OpenApiExample(
    name="Empty required fields example",
    value=error_400_empty_fields,
    response_only=True,
)

not_valid_names_example = OpenApiExample(
    name="Not valid names example",
    value=error_400_invalid_names,
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

crew_set_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of crew members, allowing filter",
        parameters=[
            OpenApiParameter(
                name="full_name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by full name or its part, case insensitive. "
                    "Use space between first and last names. "
                    "Examples: '?full_name=john', '?full_name=john doe'"
                ),
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                name="Crew list example",
                value=crew_list_json
            )
        ],
        responses={
            status.HTTP_200_OK: CrewReadSerializer(many=False),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response
        },
    ),
    create=extend_schema(
        description="Create a new crew member",
        request=CrewCreateUpdateSerializer(),
        examples=[
            crew_request_example,
            crew_response_example
        ],
        responses={
            status.HTTP_201_CREATED: CrewCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_names_example
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
        }
    ),
    retrieve=extend_schema(
        description="Retrieve detail crew member information",
        examples=[
            OpenApiExample(
                name="Crew detail example",
                value=crew_detail_json,
            )
        ],
        responses={
            status.HTTP_200_OK: CrewReadSerializer(),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        },
    ),
    update=extend_schema(
        description="Update crew member information",
        request=CrewCreateUpdateSerializer(),
        examples=[
            crew_request_example,
            crew_response_example
        ],
        responses={
            status.HTTP_200_OK: CrewCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_names_example
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    partial_update=extend_schema(
        description="Partial update crew member information",
        request=CrewCreateUpdateSerializer(partial=True),
        examples=[
            crew_request_example,
            crew_response_example
        ],
        responses={
            status.HTTP_200_OK: CrewCreateUpdateSerializer(partial=True),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    not_valid_names_example
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    destroy=extend_schema(
        description="Delete crew",
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    upload_image=extend_schema(
        description="Upload image for a crew member. Up to 1 MB. "
                    "Allowed extensions: png, jpg, jpeg",
        request=CrewImageSerializer(),
        examples=[crew_image_response_example],
        responses={
            status.HTTP_200_OK: CrewImageSerializer(),
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
