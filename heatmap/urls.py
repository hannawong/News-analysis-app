from django.urls import path

from . import views

urlpatterns = [
    path('heatmap/<cluster_id>/<starttime>/<endtime>',views.heatmap,name='heatmap'),
]