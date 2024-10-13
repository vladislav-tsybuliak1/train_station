import os
import uuid

from django.utils.text import slugify


def train_image_file_path(train, filename) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(train.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/trains/", filename)
