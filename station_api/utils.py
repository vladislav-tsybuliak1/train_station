import os
import uuid

from django.utils.text import slugify

from station_api.models import Train


def train_image_file_path(train: Train, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(train.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/movies/", filename)
