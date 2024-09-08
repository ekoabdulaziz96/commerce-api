from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "apps.app_users"
    verbose_name = "App Users"

    def ready(self):
        try:
            import apps.app_users.signals  # type: ignore # noqa: F401
        except ImportError:
            pass
