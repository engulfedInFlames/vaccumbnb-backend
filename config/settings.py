from pathlib import Path
import os
import environ

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_APPS = [
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "houses.apps.HousesConfig",
    "experiences.apps.ExperiencesConfig",
    "amenities.apps.AmenitiesConfig",
    "categories.apps.CategoriesConfig",
    "reviews.apps.ReviewsConfig",
    "wishlists.apps.WishlistsConfig",
    "bookings.apps.BookingsConfig",
    "medias.apps.MediasConfig",
    "dms.apps.DmsConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
]

INSTALLED_APPS = SYSTEM_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

PAGE_SIZE = 5

# ✅ For media files
# ↓ 업로드된 파일이 저장될 경로를 지정. 파일이 실제로 있을 위치
MEDIA_ROOT = "uploads"  # ❌ "/uploads"

# ↓ 클라이언트가 미디어 파일에 접근하려 할 때, 어떤 URL로 가야 하는지를 명시. 파일을 노출하는 방법
MEDIA_URL = "uploads/"  # "/"로 끝나야 하며, MEDIA_ROOT와 동일한 경로일 필요는 없다.
# ↑ MEDIA_URL을 설정한 후에 admin에서 해당 파일에 접근하면 지정된 url로 이동한다. 하지만 django는 해당 url에 대해서 모르기 때문에 urls.py에서 해당 경로를 노출시켜야 한다.

# ↑ 하지만 위 방법은 개발 단계에서만 사용하는 것이 권장되며, 배포 단계에서는 보안 위험(서버에 아무 파일이나 업로드되는 것) 때문에 다른 방법을 사용하는 것이 권장된다. 클라이언트가 업로드 하는 파일이 서버에 직접 저장되어서는 안 된다. 대신, django는 파일의 url만을 알게 하고, 다른 서버에 저장되게 해야 한다.  Docs의 "Serving files uploaded by a user during development" 참조.


"""
↓ Default
"DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]

1. 로그인을 시도하면 장고가 클래스 안의 인증 방식들을 차례대로 시도한다. 포스트맨에 쿠키를 담아 보내지 않으면, DRF의 인증 방식으로는 로그인할 수 없다.
2. "rest_framework.authentication.SessionAuthentication" 클래스를 사용하게 되면, CSRF 토큰 인증을 해야 한다.
"""

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
]

GITHUB_CLIENT_ID = env("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = env("GITHUB_CLIENT_SECRET")

KAKAO_ADMIN_KEY = env("KAKAO_ADMIN_KEY")
KAKAO_CLIENT_SECRET = env("KAKAO_CLIENT_SECRET")
