from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# BASE
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ------------------------------------------------------------------------------
# CORE SETTINGS
# ------------------------------------------------------------------------------

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-dev-key-change-this"
)

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost,.onrender.com,masters-spiritual.com"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://masters-spiritual.com",
    "https://*.onrender.com",
]

LOGIN_URL = "/login/"

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",

    # Utilities
    "django_summernote",
    "crispy_forms",
    "crispy_bootstrap5",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # Your apps
    "content",
    "social",
    "masters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "masters.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "masters.wsgi.application"

# ------------------------------------------------------------------------------
# DATABASE (POSTGRES — LOCAL + RENDER)
# ------------------------------------------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://mastersuser:yourpassword@localhost:5432/masters",
        conn_max_age=600,
        ssl_require=os.getenv("RENDER") is not None,
    )
}

# ------------------------------------------------------------------------------
# PASSWORDS & I18N
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# STATIC FILES (WHITENOISE)
# ------------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------------------------------------------------------
# MEDIA FILES (CLOUDINARY — FIXES MISSING POSTS)
# ------------------------------------------------------------------------------

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
MEDIA_URL = "/media/"

# ❗ DO NOT define MEDIA_ROOT when using Cloudinary

# ------------------------------------------------------------------------------
# OTHER SETTINGS
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
X_FRAME_OPTIONS = "SAMEORIGIN"

# ------------------------------------------------------------------------------
# EMAIL
# ------------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER




# from pathlib import Path
# import os
# import dj_database_url
# from dotenv import load_dotenv  # type: ignore
# # import cloudinary
# # import cloudinary.uploader
# # import cloudinary.api

# BASE_DIR = Path(__file__).resolve().parent.parent

# load_dotenv(BASE_DIR / ".env")  # <-- load variables from .env
# DEBUG = True

# # ✅ Read secret key from environment for security
# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
# if not SECRET_KEY:
#     raise RuntimeError("DJANGO_SECRET_KEY environment variable not set!")



# # ✅ Set DEBUG via environment variable (default False for safety)
# # DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

# # local
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
# # prod
# # 


# # Get hosts from environment variable, or use the default string
# # ALLOWED_HOSTS_STRING = os.environ.get(
# #     "DJANGO_ALLOWED_HOSTS",
# #     "masters-spiritual.com,www.masters-spiritual.com,masters-spiritual.onrender.com"
# # )

# # Convert the string to a list, stripping whitespace
# # ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STRING.split(",") if host]

# # --- CRITICAL ADDITIONS ---
# # 1. Add localhost for internal health checks/requests
# # ALLOWED_HOSTS.append('127.0.0.1')

# # 2. Add the dynamic external hostname provided by Render
# #    This covers the main URL and may be required for certain proxy setups.
# # render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
# # if render_host:
# #     ALLOWED_HOSTS.append(render_host)

# # Optional: Add the specific port Render uses if it's explicitly in the Host header
# # ALLOWED_HOSTS.append('0.0.0.0')
# # --------------------------

# # Print to logs to verify during deployment (optional, but helpful)
# # print(f"DEBUG: ALLOWED_HOSTS is set to: {ALLOWED_HOSTS}")





# # --------------------------------------------------------------------------
# # APPLICATION DEFINITION
# # --------------------------------------------------------------------------

# LOGIN_URL = '/login/'  # or your login path

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sites',

#     # Allauth
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     'allauth.socialaccount.providers.google',
#     'allauth.socialaccount.providers.facebook',

#     # Utilities
#     'django_summernote',
#     'crispy_forms',
#     'crispy_bootstrap5',

#     # Your apps
#     'content',
#     'social',
#     'masters'
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ WhiteNoise enabled
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',

#     # Allauth
#     "allauth.account.middleware.AccountMiddleware",
# ]

# ROOT_URLCONF = 'masters.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, "templates")],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'masters.wsgi.application'

# # --------------------------------------------------------------------------
# # DATABASE, AUTH, and I18N
# # --------------------------------------------------------------------------
# ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# DATABASES = {
#     "default": dj_database_url.config(
#         default="postgresql://postgres:postgres@localhost:5432/masters",  # local fallback
#         conn_max_age=600,
#         ssl_require=os.getenv("RENDER") is not None,  # only require SSL on Render
#     )
# }

# # Cloudinary config
# # cloudinary.config(
# #     cloud_name=os.getenv("CLOUD_NAME"),
# #     api_key=os.getenv("CLOUDINARY_API_KEY"),
# #     api_secret=os.getenv("CLOUDINARY_API_SECRET"),
# #     secure=True,
# # )

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'masters',
#         'USER': 'mastersuser',
#         'PASSWORD': 'yourpassword',  # replace with the password you set in psql
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }





# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # --------------------------------------------------------------------------
# # STATIC & MEDIA FILES
# # --------------------------------------------------------------------------
# # 🔹 Static files
# STATIC_URL = "/static/"
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATIC_ROOT = BASE_DIR / "staticfiles"

# # WhiteNoise storage backend for production (for static files only)
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# # 🔹 Cloudinary Media Storage
# # CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
# # DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# # (You don’t need MEDIA_ROOT if using Cloudinary)
# # 🔹 Media files
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"


# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# # --------------------------------------------------------------------------
# # CUSTOM & THIRD-PARTY SETTINGS
# # --------------------------------------------------------------------------

# X_FRAME_OPTIONS = 'SAMEORIGIN'
# SUMMERNOTE_CONFIG = {
#     'summernote': {'width': '100%', 'height': '400px'},
#     'attachment_require_authentication': True,
# }

# SESSION_ENGINE = "django.contrib.sessions.backends.db"

# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5"
# SITE_ID = 1

# # --------------------------------------------------------------------------
# # EMAIL SETTINGS
# # --------------------------------------------------------------------------
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "greatestevermasters@gmail.com"  # replace with your email
# EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD  # replace with app password
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # --------------------------------------------------------------------------
# # SECURITY & YOUTUBE COMPATIBILITY SETTINGS (The Solution)
# # --------------------------------------------------------------------------

# # 1. Content Security Policy (CSP) for all YouTube domains
# CSP_FRAME_SRC = (
#     "'self'",
#     'https://www.youtube.com',
#     'https://www.youtube-nocookie.com',  # Privacy-enhanced domain
#     'https://youtu.be'
# )

# CSP_SCRIPT_SRC = (
#     "'self'",
#     'https://www.youtube.com',
#     'https://s.ytimg.com'  # YouTube's static assets domain
# )

# # 2. Referrer Policy for strict YouTube security checks
# # Forces the browser to send the Referer header, often required for playback permission
# SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
