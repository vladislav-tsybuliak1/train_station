import re

from django.core.exceptions import ValidationError


def validate_latitude(value: float) -> None:
    if not -90 < value < 90:
        raise ValidationError("Latitude must be between -90 and 90 degrees.")


def validate_longitude(value: float) -> None:
    if not -180 < value < 180:
        raise ValidationError(
            "Longitude must be between -180 and 180 degrees."
        )


def validate_name(name: str) -> None:
    if re.search(r"^[a-zA-Z]*$", name) is None:
        raise ValidationError(f"{name} contains non-english letters")


def validate_image_size(file) -> None:
    filesize = file.size
    max_upload_size = 1 * 1024 * 1024

    if filesize > max_upload_size:
        raise ValidationError("The image size should be less than 1 MB")
