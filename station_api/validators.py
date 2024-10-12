from django.core.exceptions import ValidationError


def validate_latitude(value: float) -> None:
    if -90 < value < 90:
        raise ValidationError("Latitude must be between -90 and 90 degrees.")

def validate_longitude(value: float) -> None:
    if -180 < value < 180:
        raise ValidationError(
            "Longitude must be between -180 and 180 degrees."
        )
