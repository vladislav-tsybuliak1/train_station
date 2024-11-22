from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiResponse
)
from rest_framework import status

from station_api.schemas.examples.common_responses import (
    unauthorized_response,
    forbidden_response,
)
from station_api.schemas.examples.orders import (
    order_list_json,
    order_create_request_json,
    order_create_response_json,
    error_400_empty_fields,
    error_400_invalid_place
)
from station_api.serializers import OrderListSerializer, OrderSerializer


order_list_create_schema = extend_schema_view(
    list=extend_schema(
        description="Retrieve list of authorised user orders",
        examples=[
            OpenApiExample(
                name="Order list example",
                value=order_list_json
            )
        ],
        responses={
            status.HTTP_200_OK: OrderListSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response
        },
    ),
    create=extend_schema(
        description="Create a new order",
        request=OrderSerializer(),
        examples=[
            OpenApiExample(
                name="Order request example",
                value=order_create_request_json,
                request_only=True,
            ),
            OpenApiExample(
                name="Order response example",
                value=order_create_response_json,
                response_only=True,
            )
        ],
        responses={
            status.HTTP_201_CREATED: OrderSerializer(),
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
                        name="Not unique (cargo, seat, trip) example",
                        value=error_400_invalid_place,
                        response_only=True,
                    )
                ]
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
        }
    )
)
