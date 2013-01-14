from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils.http import urlquote
import os

from django.conf import settings

#For no-XSendfile approach
from django.core.servers.basehttp import FileWrapper

def send(request, file):
    if not file:
        raise Http404

    if settings.LASANA_USE_X_SENDFILE:
        response = HttpResponse()
        response['Content-Disposition'] = 'filename=%s' % urlquote(os.path.basename(file.name))
        response['X-Sendfile'] = file.path
        return response
    else:
        response = HttpResponse(FileWrapper(file))
        response['Content-Disposition'] = 'filename=%s' % urlquote(os.path.basename(file.name))
        del response['content-type'] #let the web server guess
        response['Content-Length'] = file.size
        return response
