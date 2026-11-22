from django.apps import AppConfig


class BuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder'
    verbose_name = "BUYURTMALAR VA SOZLAMALAR"

    def ready(self):
        from . import signals  # noqa: F401

