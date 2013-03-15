from . import settings

def common(request):
    return {'lasana_name': settings.LASANA_NAME}
