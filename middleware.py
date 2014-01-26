# Enabling this middleware you can force browsers with good SSL support to use
# HTTPS, while making it optional for other legacy applications with limited or
# no SSL support.

from django.http import HttpResponseRedirect
from django.conf import settings

import re

browser_strings = [
    'Firefox',
    'Iceweasel',
    'Chrome',
    'Opera',
    'Trident',
    'Safari',
    'Konqueror',
]

re_http = re.compile(r'^http:')

def is_a_browser(user_agent):
    return any(browser in user_agent
               for browser in browser_strings)


class ForceHTTPSOnBrowsersMiddleware(object):
    def process_request(self, request):
        # Disable on DEBUG
        if settings.DEBUG:
            return

        # Skip if the request is already HTTPS
        if request.is_secure():
            return

        # Only redirect GET requests
        if request.method != 'GET':
            return
  
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if is_a_browser(request.META['HTTP_USER_AGENT']):
            url = request.build_absolute_uri()
            url = re_http.sub('https:', url)
            return HttpResponseRedirect(url)
