from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, OpenApiExample

from station_api.schemas.examples.common_errors import (
    error_401_unauthorized,
    error_403_forbidden
)


unauthorized_response = OpenApiResponse(
    description="Unauthorized",
    response=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            name="Unauthorized example",
            value=error_401_unauthorized,
            response_only=True,
        ),
    ]
)

forbidden_response = OpenApiResponse(
    description="Forbidden",
    response=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            name="Forbidden example",
            value=error_403_forbidden,
            response_only=True,
        ),
    ]
)
