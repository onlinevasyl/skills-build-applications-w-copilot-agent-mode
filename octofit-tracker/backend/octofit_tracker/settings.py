import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "local-development-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

INSTALLED_APPS = [
    "corsheaders",
    "octofit_tracker.apps.OctoFitTrackerConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "octofit_tracker.urls"
TEMPLATES = []
WSGI_APPLICATION = "octofit_tracker.wsgi.application"
ASGI_APPLICATION = "octofit_tracker.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django_mongodb_backend",
        "HOST": os.environ.get("MONGODB_URI", "mongodb://localhost:27017"),
        "NAME": os.environ.get("MONGODB_NAME", "octofit_db"),
    }
}

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"
