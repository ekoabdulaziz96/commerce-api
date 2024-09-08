from django.apps import AppConfig


class AppCommerceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.app_commerce"

    def ready(self):
        try:
            import apps.app_commerce.signals  # type: ignore # noqa: F401
        except ImportError:
            pass
