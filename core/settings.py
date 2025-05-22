import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

# -------------------------------------------------------------------
# BASE_DIR & .env
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# -------------------------------------------------------------------
# SECRET_KEY & DEBUG
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG      = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = get_random_secret_key()
        sys.stderr.write("⚠️  DJANGO_SECRET_KEY manquante, utilisation d'une clé aléatoire en DEBUG\n")
    else:
        raise RuntimeError(
            "🛑 DJANGO_SECRET_KEY introuvable : créez un fichier .env "
            "à la racine avec DJANGO_SECRET_KEY=…"
        )

# -------------------------------------------------------------------
# ALLOWED_HOSTS
# -------------------------------------------------------------------
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1").split()

# -------------------------------------------------------------------
# INSTALLED_APPS
# -------------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_filters",
    "django_extensions",
    # Internal
    "geodata",
    "accounts",
    "units",
    "activities",
]

# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # pour dev
    "https://e-dpvn.org",      # prod
    "https://www.e-dpvn.org",
]

# -------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# -------------------------------------------------------------------
# DATABASES (PostgreSQL)
# -------------------------------------------------------------------
_db_host = os.getenv("DB_HOST", "localhost")
if DEBUG and _db_host.lower() == "db":
    _db_host = "localhost"

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     os.getenv("DB_NAME"),
        "USER":     os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST":     _db_host,
        "PORT":     os.getenv("DB_PORT", "5432"),
    }
}

# -------------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------------------------
# INTERNATIONALISATION
# -------------------------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE     = "Africa/Niamey"
USE_I18N      = True
USE_TZ        = True

# -------------------------------------------------------------------
# STATIC & MEDIA FILES -- ABSOLUTE PATHS !
# -------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = "/srv/e-dpvn-backend/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = "/srv/e-dpvn-backend/media/"

# -------------------------------------------------------------------
# SÉCURITÉ POUR LA PROD (SSL)
# -------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# -------------------------------------------------------------------
# DEFAULT PK & AUTH_USER_MODEL
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL    = "accounts.User"

# -------------------------------------------------------------------
# DRF & drf-spectacular
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
    "TITLE":       "e-DPVN API",
    "DESCRIPTION": "Documentation de l’API e-DPVN",
    "VERSION":     "1.0.0",
}
