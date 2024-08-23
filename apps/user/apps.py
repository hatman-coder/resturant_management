from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user"

    def ready(self):
        import signals.user_permission
