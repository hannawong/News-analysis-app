'''
meeting URL Configuration
'''
from django.urls import path

from .views import index


urlpatterns = [
    path('', index),
]