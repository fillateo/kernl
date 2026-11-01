"""Django settings for the Kernl learning platform.

Everything runs locally by default: SQLite for persistence, an in-memory
Channels layer for WebSockets, and bubblewrap for isolated terminal sessions.
No third-party service credentials are required.
"""

from pathlib import Path

import environ

# backend/config/settings.py -> repository root
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CORS_ALLOWED_ORIGINS=(
        list,
        ["http://localhost:3000", "http://127.0.0.1:3000"],
    ),
    CSRF_TRUSTED_ORIGINS=(
        list,
        ["http://localhost:3000", "http://127.0.0.1:3000"],
    ),
    TERMINAL_SESSION_TTL_SECONDS=(int, 30 * 60),
    TERMINAL_IDLE_TIMEOUT_SECONDS=(int, 10 * 60),
    TERMINAL_MAX_LIFETIME_SECONDS=(int, 20 * 60),
    TERMINAL_MAX_SESSIONS=(int, 25),
    TERMINAL_MAX_OUTPUT_BYTES=(int, 2 * 1024 * 1024),
)

for env_file in (ROOT_DIR / ".env", BASE_DIR / ".env"):
    if env_file.exists():
        env.read_env(env_file)

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-kernl-local-development-key-change-me",
)
DEBUG = env.bool("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# Application definition -----------------------------------------------------

DJANGO_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "channels",
    "corsheaders",
    "rest_framework",
]

LOCAL_APPS = [
    "apps.catalog",
    "apps.terminal",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES: list[dict] = []

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database -------------------------------------------------------------------

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DB_CONN_MAX_AGE", default=0)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization -------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and media files -----------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Let Whitenoise serve admin/static assets from the app finders during local
# development without requiring a collectstatic step.
WHITENOISE_USE_FINDERS = DEBUG

# REST API -------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_PAGINATION_CLASS": None,
    "DEFAULT_THROTTLE_RATES": {
        "terminal_session": env("TERMINAL_SESSION_THROTTLE", default="20/min"),
    },
}

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = False
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Channels -------------------------------------------------------------------
# Each terminal consumer sends directly to its own WebSocket and does not use
# channel groups, so the in-memory layer is sufficient across Uvicorn workers.
# Add a shared layer such as Redis if cross-worker group messaging is introduced.

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# Interactive terminal -------------------------------------------------------

TERMINAL_SESSION_TTL_SECONDS = env.int("TERMINAL_SESSION_TTL_SECONDS")
TERMINAL_IDLE_TIMEOUT_SECONDS = env.int("TERMINAL_IDLE_TIMEOUT_SECONDS")
TERMINAL_MAX_LIFETIME_SECONDS = env.int("TERMINAL_MAX_LIFETIME_SECONDS")
TERMINAL_MAX_SESSIONS = env.int("TERMINAL_MAX_SESSIONS")
TERMINAL_MAX_OUTPUT_BYTES = env.int("TERMINAL_MAX_OUTPUT_BYTES")
TERMINAL_WORK_ROOT = Path(
    env("TERMINAL_WORK_ROOT", default=str(BASE_DIR / "var" / "terminal"))
)
TERMINAL_SHELL_CLASS = env(
    "TERMINAL_SHELL_CLASS",
    default="apps.terminal.services.bubblewrap.BubblewrapShell",
)

# Security -------------------------------------------------------------------

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)

# Logging --------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("DJANGO_LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django.server": {"level": "WARNING"},
        "apps.terminal": {"level": env("TERMINAL_LOG_LEVEL", default="INFO")},
    },
}
