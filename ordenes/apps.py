from django.apps import AppConfig


class OrdenesConfig(AppConfig):
    name = 'ordenes'

    def ready(self):
        # Import signals to ensure they are registered
        from . import signals  # noqa: F401
