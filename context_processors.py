from django.conf import settings
from . settings import LASANA_NAME, LASANA_DEFAULT_STYLE
from . import styles
import re

basic_name = re.compile(r'^[a-zA-Z0-9_]+$')

def common(request):
    style = styles.get_style(request)
    stylesheet = settings.STATIC_URL + 'lasana/css/%s.css' % style

    return {
        'lasana_name': LASANA_NAME,
        'style'      : style,
        'stylesheet' : stylesheet,
        }
