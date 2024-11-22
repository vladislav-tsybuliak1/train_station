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
from station_api.schemas.examples.trips import (
    trip_list_json,
    trip_create_update_request_json,
    trip_create_update_response_json,
    error_400_empty_fields,
    error_400_invalid_route,
    error_400_invalid_train,
    error_400_invalid_crew,
    error_400_arrival_time_before_departure_time,
    trip_detail_json,
    error_404_not_found
)
from station_api.serializers import (
    TripListSerializer,
    TripCreateUpdateSerializer, TripRetrieveSerializer,
)


trip_request_example = OpenApiExample(
    name="Trip request example",
    value=trip_create_update_request_json,
    request_only=True,
)

trip_response_example = OpenApiExample(
    name="Trip response example",
    value=trip_create_update_response_json,
    response_only=True,
)

empty_fields_example = OpenApiExample(
    name="Empty required fields example",
    value=error_400_empty_fields,
    response_only=True,
)

not_valid_route_example = OpenApiExample(
    name="Not valid route example",
    value=error_400_invalid_route,
    response_only=True,
)

not_valid_train_example = OpenApiExample(
    name="Not valid train example",
    value=error_400_invalid_train,
    response_only=True,
)

not_valid_crew_example = OpenApiExample(
    name="Not valid crew example",
    value=error_400_invalid_crew,
    response_only=True,
)

arrival_time_before_departure_time_example = OpenApiExample(
    name="Arrival time before departure time example",
    value=error_400_arrival_time_before_departure_time,
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


trip_set_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of trips, allowing filter",
        parameters=[
            OpenApiParameter(
                name="departure_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by departure date. Format: YYYY-MM-DD. "
                    "Example: '?departure_date=2024-10-15'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="source_station",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by source station name. Case insensitive. "
                    "Example: '?source_station=chernivtsi'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="destination_station",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by destination station name. Case insensitive. "
                    "Example: '?destination_station=kyiv'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="train_type",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by train type name or its part. Case insensitive. "
                    "Example: '?train_type=night'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="tickets_available",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter trips that have available tickets. "
                    "Example: '?tickets_available=true'"
                ),
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                name="Trip list example",
                value=trip_list_json
            )
        ],
        responses={
            status.HTTP_200_OK: TripListSerializer(many=False),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response
        },
    ),
    create=extend_schema(
        description="Create a new trip",
        request=TripCreateUpdateSerializer(),
        examples=[
            trip_request_example,
            trip_response_example
        ],
        responses={
            status.HTTP_201_CREATED: TripCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_route_example,
                    not_valid_crew_example,
                    not_valid_train_example,
                    arrival_time_before_departure_time_example
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
        },
    ),
    retrieve=extend_schema(
        description="Retrieve detail trip information",
        examples=[
            OpenApiExample(
                name="Trip detail example",
                value=trip_detail_json,
            )
        ],
        responses={
            status.HTTP_200_OK: TripRetrieveSerializer(),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        },
    ),
    update=extend_schema(
        description="Update trip information",
        request=TripCreateUpdateSerializer(),
        examples=[
            trip_request_example,
            trip_response_example
        ],
        responses={
            status.HTTP_200_OK: TripCreateUpdateSerializer(),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    not_valid_route_example,
                    not_valid_crew_example,
                    not_valid_train_example,
                    arrival_time_before_departure_time_example
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    partial_update=extend_schema(
        description="Partial update trip information",
        request=TripCreateUpdateSerializer(partial=True),
        examples=[
            trip_request_example,
            trip_response_example
        ],
        responses={
            status.HTTP_200_OK: TripCreateUpdateSerializer(partial=True),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    not_valid_route_example,
                    not_valid_crew_example,
                    not_valid_train_example,
                    arrival_time_before_departure_time_example
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
    destroy=extend_schema(
        description="Delete trip",
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
            status.HTTP_404_NOT_FOUND: not_found_response,
        }
    ),
)
