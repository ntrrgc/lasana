from django.conf import settings
from . settings import LASANA_NAME
from . import styles
import re

basic_name = re.compile(r'^[a-zA-Z0-9_]+$')

def common(request):
    style = styles.get_style(request)
    stylesheet = settings.STATIC_URL + 'lasana/css/%s.css' % (style or 'default')

    return {
        'lasana_name': LASANA_NAME,
        'style'      : style,
        'stylesheet' : stylesheet,
        }
