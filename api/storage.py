
from django.conf import settings

def upload(file, photo):
    settings.storage.child(file).put(photo)
    url = settings.storage.child(file).get_url(None)
    return url

def delete(file):
    settings.storage.delete(file, 'fake')