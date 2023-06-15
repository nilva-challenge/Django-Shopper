# Application definition
LOCAL_APPS = [
    "apps.user",
    "apps.product"
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
]

DEFAULT_APPS = [
    # base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = (
        DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS
)
