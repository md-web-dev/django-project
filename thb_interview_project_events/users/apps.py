from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "thb_interview_project_events.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import thb_interview_project_events.users.signals  # noqa F401
        except ImportError:
            pass
