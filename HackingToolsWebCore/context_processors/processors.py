import os


def get_backend_url(request):
    return {'WEB_URL': os.getenv('WEB_URL')}
