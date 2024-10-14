import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from station_api.models import Crew, Train


@receiver(pre_delete, sender=Crew)
def delete_crew_image(sender, instance, **kwargs) -> None:
    if os.path.isfile(instance.crew_image.path):
        os.remove(instance.crew_image.path)


@receiver(pre_delete, sender=Train)
def delete_train_image(sender, instance, **kwargs) -> None:
    if os.path.isfile(instance.train_image.path):
        os.remove(instance.train_image.path)
