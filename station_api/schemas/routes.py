from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)

from station_api.schemas.examples.common_responses import (
    unauthorized_response,
    forbidden_response
)
from station_api.schemas.examples.routes import (
    route_list_json,
    route_create_update_request_json,
    route_create_update_response_json,
    route_detail_json,
    error_400_empty_fields,
    error_400_not_valid_distance,
    error_400_same_source_destination,
    error_400_invalid_source_destination,
    error_404_not_found,
)
from station_api.serializers import (
    RouteReadSerializer,
    RouteCreateUpdateSerializer,
)

route_request_example = OpenApiExample(
    name="Route request example",
    value=route_create_update_request_json,
    request_only=True,
)

route_response_example = OpenApiExample(
    name="Route response example",
    value=route_create_update_response_json,
    response_only=True,
)

empty_fields_example = OpenApiExample(
    name="Empty required fields example",
    value=error_400_empty_fields,
    response_only=True,
)

same_source_and_destination_example = OpenApiExample(
    name="The same source and destination example",
    value=error_400_same_source_destination,
    response_only=True,
)

not_valid_distance_example = OpenApiExample(
    name="Not valid distance example",
    value=error_400_not_valid_distance,
    response_only=True,
)

not_valid_source_destination = OpenApiExample(
    name="Not valid source/destination example",
    value=error_400_invalid_source_destination,
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

route_set_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of routes, allowing filter",
        parameters=[
            OpenApiParameter(
                name="source",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by source name or its part, case insensitive. "
                    "Example: '?source=chernivtsi'"
                ),
                required=False,
            ),
            OpenApiParameter(
                name="destination",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Filter by destination name or its part, case insensitive. "
                    "Example: '?destination=chernivtsi'"
                ),
                required=False,
            )
        ],
        examples=[
            OpenApiExample(
                name="Route list example",
                value=route_list_json
            )
        ],
        responses={
            200: RouteReadSerializer(),
            401: unauthorized_response
        },
    ),
    create=extend_schema(
        description="Create a new route",
        request=RouteCreateUpdateSerializer(),
        examples=[
            route_request_example,
            route_response_example
        ],
        responses={
            201: RouteCreateUpdateSerializer(),
            400: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    same_source_and_destination_example,
                    not_valid_distance_example,
                    not_valid_source_destination
                ]
            ),
            401: unauthorized_response,
            403: forbidden_response,
        }
    ),
    retrieve=extend_schema(
        description="Retrieve detail route information",
        examples=[
            OpenApiExample(
                name="Route detail example",
                value=route_detail_json,
            )
        ],
        responses={
            200: RouteReadSerializer(),
            401: unauthorized_response,
            404: not_found_response,
        },
    ),
    update=extend_schema(
        description="Update route information",
        request=RouteCreateUpdateSerializer(),
        examples=[
            route_request_example,
            route_response_example
        ],
        responses={
            201: RouteCreateUpdateSerializer(),
            400: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    empty_fields_example,
                    same_source_and_destination_example,
                    not_valid_distance_example,
                    not_valid_source_destination
                ]
            ),
            401: unauthorized_response,
            403: forbidden_response,
            404: not_found_response,
        }
    ),
    partial_update=extend_schema(
        description="Partial update route information",
        request=RouteCreateUpdateSerializer(partial=True),
        examples=[
            route_request_example,
            route_response_example
        ],
        responses={
            201: RouteCreateUpdateSerializer(partial=True),
            400: OpenApiResponse(
                description="Bad request, invalid data",
                response=OpenApiTypes.OBJECT,
                examples=[
                    same_source_and_destination_example,
                    not_valid_distance_example,
                    not_valid_source_destination
                ]
            ),
            401: unauthorized_response,
            403: forbidden_response,
            404: not_found_response,
        }
    ),
    destroy=extend_schema(
        description="Delete route",
        responses={
            204: None,
            401: unauthorized_response,
            403: forbidden_response,
            404: not_found_response,
        }
    )
)
