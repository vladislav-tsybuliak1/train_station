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
from station_api.schemas.examples.stations import (
    station_list_json,
    station_create_request_json,
    station_create_response_json,
    error_400_empty_fields,
    error_400_same_station_name,
    error_400_not_valid_latitude_and_longitude
)
from station_api.serializers import StationSerializer


station_list_create_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of stations, allowing filter",
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by station name or its part, case insensitive. "
                    "Example: '?name=chernivtsi'"
                ),
                required=False,
            )
        ],
        examples=[
            OpenApiExample(
                name="Station list example",
                value=station_list_json,
            )
        ],
        responses={
            status.HTTP_200_OK: StationSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response
        },
    ),
    create=extend_schema(
        description="Create a new station",
        request=StationSerializer(),
        examples=[
            OpenApiExample(
                name="Station request example",
                value=station_create_request_json,
                request_only=True,
            ),
            OpenApiExample(
                name="Station response example",
                value=station_create_response_json,
                response_only=True,
            )
        ],
        responses={
            status.HTTP_201_CREATED: StationSerializer(),
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
                        name="Not unique station name example",
                        value=error_400_same_station_name,
                        response_only=True,
                    ),
                    OpenApiExample(
                        name="Not valid latitude and longitude example",
                        value=error_400_not_valid_latitude_and_longitude,
                        response_only=True,
                    ),
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
        }
    )
)
