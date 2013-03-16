from django.conf import settings
from . settings import LASANA_NAME
import re

basic_name = re.compile(r'^[a-zA-Z0-9_]+$')

def common(request):
    style = request.GET.get('style')
    if style is not None:
        # Only allow style names with letters, numbers and underscore
        if not basic_name.match(style):
            style = None

    stylesheet = settings.STATIC_URL + 'lasana/css/%s.css' % (style or 'default')

    return {
        'lasana_name': LASANA_NAME,
        'stylesheet' : stylesheet,
        }
