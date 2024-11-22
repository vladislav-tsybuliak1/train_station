import os
import uuid

from django.utils.text import slugify


def train_image_file_path(train, filename) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(train.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/trains/", filename)


def crew_image_file_path(crew, filename) -> str:
    _, extension = os.path.splitext(filename)
    filename = (
        f"{slugify(crew.first_name)}"
        f"-{slugify(crew.last_name)}"
        f"-{uuid.uuid4()}{extension}"
    )
    return os.path.join("uploads/crew/", filename)
