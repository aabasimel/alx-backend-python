from django.apps import AppConfig


# pylint: disable=unused-import
class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"

    def ready(self):
        import messaging.signals