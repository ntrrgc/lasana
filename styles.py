import re
from . settings import LASANA_DEFAULT_STYLE

basic_name = re.compile(r'^[a-zA-Z0-9_]+$')

def is_basic_name(style):
    # Only allow style names with letters, numbers and underscore
    return bool(basic_name.match(style))

def get_style(request):
    style_from_session = request.session.get('style')

    style_from_get = request.GET.get('style')
    if style_from_get and not is_basic_name(style_from_get):
        style_from_get = None

    return style_from_get or style_from_session or LASANA_DEFAULT_STYLE

def set_style(request, style):
    if style and is_basic_name(style):
        request.session['style'] = style
