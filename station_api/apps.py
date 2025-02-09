from django.apps import AppConfig


class StationApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "station_api"

    def ready(self) -> None:
        import station_api.signals
