from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

urlpatterns = [
    path('index0',views.message,name='index0'),
    path('search/',views.search, name='search')
]

# router = SimpleRouter()
# router.register(r'search', views.ArticleSearchViewSet, basename='search')
# urlpatterns += router.urls
