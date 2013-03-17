# -*- encoding: utf-8 -*-
from django.conf import settings

def get(key, default):
    return getattr(settings, key, default)

LASANA_NAME = get('LASANA_NAME', u'Lasaña')
