
from django.conf import settings
import pyrebase
import os 

firebase = pyrebase.initialize_app(settings.FIREBASECONFIG)
storage = firebase.storage()

def upload(file, photo):
    storage.child(file).put(photo)
    url = storage.child(file).get_url(None)
    return url

def delete(file):
    storage.delete(file, 'fake')