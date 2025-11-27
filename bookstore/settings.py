
from pathlib import Path
import os
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-m4dla30faa0w+4mzzn^op9_3rkz@9#^3v4vr96v0)c#8ratso0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.ngrok-free.app',
    '.ngrok-free.dev',
    'heterolecithal-grant-unrecommended.ngrok-free.dev',
]
if DEBUG:
    ip = "http://127.0.0.1:8000"
    # ip = "http://destiny.soprada.com/"
    # ip = "https://www.api.destinybookshub.com/"
else:
    # ip = "http://destiny.soprada.com/"
    ip = "https://www.api.destinybookshub.com/"

# Application definition
# SOCIAL_AUTH_URL_NAMESPACE = 'social'
INSTALLED_APPS = [
    'dashub',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dashboard",
    "order",
    # "payment",
    "product",
    "user_accounts",
    "website",
    'rest_framework',
    'rest_framework_simplejwt',
    'inventory',
    'django_summernote',
    'corsheaders',
    'social_django',
    'rest_framework_social_oauth2',
    'oauth2_provider',
    'blog',

]

CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok-free.dev',
    'https://heterolecithal-grant-unrecommended.ngrok-free.dev',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = "bookstore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR / 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = "bookstore.wsgi.application"

AUTH_USER_MODEL = "user_accounts.CustomUser"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Kathmandu'


USE_I18N = True
LOGIN_REDIRECT_URL = 'home'
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
        
        BASE_DIR / "static",
    ]
    STATIC_ROOT = BASE_DIR / 'staticfiles'
else:
    STATIC_ROOT = BASE_DIR / 'static'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Allow embedding in iframes from any origin
X_FRAME_OPTIONS = 'ALLOWALL'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    
    'django.contrib.auth.backends.ModelBackend',

    # 'rest_framework_social_oauth2.backends.DjangoOAuth2',
)

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
        

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]

}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'JWT_EXPIRATION_DELTA':datetime.timedelta(days=2),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    # 'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
    'USER_ID_FIELD': 'uuid',
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


CORS_ORIGINS_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

# for email
if DEBUG:
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'destinybookshub@gmail.com'
EMAIL_HOST_PASSWORD = 'oajr txdz jevl ynxg'




# load_dotenv()

CORS_ORIGINS_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True


DASHUB_SETTINGS = {
    "site_logo": "/static/logo.png",
    "site_icon": "/static/favicon.ico",
    "theme_color": "#198CD9",
    "border_radius": "5px",
    "hide_models": [
        "auth",  # Hides all models in the auth app
        "auth.group",  # Hides the group model in the auth app
        "django_summernote",
        "oauth2_provider",
        "rest_framework_social_oauth2",
        "social_django",
        "python social auth",
        "django oauth toolkit",
    ],
    "custom_links": {
        "auth": [
            {
                "model": "auth.post" # Links directly to the auth.post model
            },
            {
                "name": "User Management",
                "icon": "fa-solid fa-users",
                "submenu": [
                    {"model": "auth.user", "order": 1},
                    {"model": "auth.group", "order": 2}
                ]
            }
        ],
    },
    "submenus_models": ["auth.group"],
    "default_orders": {
        "auth": 10,
        "auth.group": 4,
    },
    "icons": {
        "auth": "fa-regular fa-user",
        "auth.user": "fa-regular fa-user",
        "blog.blogcategory": "fa-solid fa-list",
        "blog.blog": "fa-solid fa-blog",
        "blog.comment": "fa-solid fa-comment",
        "dashboard.newsletteremail": "fa-solid fa-envelope",
        "inventory.supplierdata": "fa-solid fa-truck-field",
        "inventory.supply": "fa-solid fa-dolly",
        "order.orderquantity": "fa-solid fa-cart-shopping",
        "order.customeraddress": "fa-solid fa-address-card",
        "order.paymentdetail": "fa-solid fa-credit-card",
        "order.orders": "fa-solid fa-box",
        "product.category": "fa-solid fa-tags",
        "product.subcategory": "fa-solid fa-tag",
        "product.author": "fa-solid fa-user-pen",
        "product.coupon": "fa-solid fa-percent",
        "product.product": "fa-solid fa-box",
        "product.tag": "fa-solid fa-hashtag",
        "product.review": "fa-solid fa-star",
        "product.productqueries": "fa-solid fa-circle-question",
        "product.wishlist": "fa-solid fa-heart",
        "user_accounts.customuser": "fa-solid fa-user",
        "user_accounts.social": "fa-solid fa-share-nodes",
        "website.carousal": "fa-solid fa-images",
        "website.faqstopic": "fa-solid fa-clipboard-question",
        "website.faqs": "fa-solid fa-circle-question",
        "website.menus": "fa-solid fa-bars",
        "website.careers": "fa-solid fa-briefcase",
        "website.newsletter": "fa-solid fa-envelope-open-text",
        "website.termsandcondition": "fa-solid fa-file-contract",
        "website.privacypolicy": "fa-solid fa-shield-halved",
    },
    "custom_js": [
        "/static/js/admin.js",
    ],
    "custom_css": [
        "/static/css/admin.css",
    ]
}