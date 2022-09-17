from django.apps import AppConfig


class FbApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fb_api'

    def ready(self):
            from . import signals
