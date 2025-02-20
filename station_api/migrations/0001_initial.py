# Generated by Django 5.1.2 on 2024-10-13 17:51

import django.core.validators
import station_api.utils
import station_api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Crew",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=63, validators=[station_api.validators.validate_name]
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=63, validators=[station_api.validators.validate_name]
                    ),
                ),
            ],
            options={
                "ordering": ("first_name", "last_name"),
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Route",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "distance",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=63, unique=True)),
                (
                    "latitude",
                    models.FloatField(
                        validators=[station_api.validators.validate_latitude]
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        validators=[station_api.validators.validate_longitude]
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cargo", models.PositiveSmallIntegerField()),
                ("seat", models.PositiveSmallIntegerField()),
            ],
            options={
                "ordering": ("trip", "cargo", "seat"),
            },
        ),
        migrations.CreateModel(
            name="Train",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=63)),
                ("cargo_num", models.PositiveSmallIntegerField()),
                ("places_in_cargo", models.PositiveSmallIntegerField()),
                (
                    "train_image",
                    models.ImageField(
                        upload_to=station_api.utils.train_image_file_path,
                        validators=[
                            station_api.validators.validate_image_size,
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png"]
                            ),
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TrainType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=63, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("departure_time", models.DateTimeField()),
                ("arrival_time", models.DateTimeField()),
            ],
            options={
                "ordering": ("departure_time",),
            },
        ),
    ]
