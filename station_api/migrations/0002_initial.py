# Generated by Django 5.1.2 on 2024-10-13 17:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("station_api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="route",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="destination_routes",
                to="station_api.station",
            ),
        ),
        migrations.AddField(
            model_name="route",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="source_routes",
                to="station_api.station",
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="station_api.order",
            ),
        ),
        migrations.AddField(
            model_name="train",
            name="train_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trains",
                to="station_api.traintype",
            ),
        ),
        migrations.AddField(
            model_name="trip",
            name="crew",
            field=models.ManyToManyField(related_name="trips", to="station_api.crew"),
        ),
        migrations.AddField(
            model_name="trip",
            name="route",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trips",
                to="station_api.route",
            ),
        ),
        migrations.AddField(
            model_name="trip",
            name="train",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trips",
                to="station_api.train",
            ),
        ),
        migrations.AddField(
            model_name="ticket",
            name="trip",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="station_api.trip",
            ),
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("cargo", "seat", "trip"), name="unique_cargo_seat_trip"
            ),
        ),
    ]
