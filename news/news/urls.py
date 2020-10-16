from django.urls import path

from . import views

urlpatterns = [
    path('index0',views.message,name='index0'),
]