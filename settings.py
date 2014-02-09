# -*- encoding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Force style names to appear in translation
_("Original")
_("Cute")
_("Dark")

def get(key, default):
    return getattr(settings, key, default)

LASANA_NAME = get('LASANA_NAME', u'Lasaña')

LASANA_DEFAULT_STYLE = get('LASANA_DEFAULT_STYLE', 'original')

LASANA_ALLOW_CHANGE_STYLE = get('LASANA_ALLOW_CHANGE_STYLE', True)

LASANA_USE_X_SENDFILE = get('LASANA_USE_X_SENDFILE', False)

LASANA_UPLOAD_ROOT = get('LASANA_UPLOAD_ROOT', './uploads')

LASANA_NGINX_ACCEL_REDIRECT_BASE_URL = get('LASANA_NGINX_ACCEL_REDIRECT_BASE_URL', '/__uploads/')

# Forbid crawlers to index user content
LASANA_BLOCK_CRAWLERS = get('LASANA_BLOCK_CRAWLERS', [
    'Googlebot',
    'YandexBot',
    'YandexImages',
    'AhrefsBot',
    'Slurp', # Yahoo
    'msnbot-media',
    'bingbot',
    'rogerbot',
    'finbot',
    'MJ12bot',
    'spbot',
])
