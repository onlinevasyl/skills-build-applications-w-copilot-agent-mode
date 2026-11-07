from django.apps import AppConfig


class OctoFitTrackerConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "octofit_tracker"
