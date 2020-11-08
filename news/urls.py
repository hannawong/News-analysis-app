from django.urls import path
from . import views

urlpatterns = [
    path('index0',views.message,name='index0'),
    path('wordcloud/<cluster_id>/<topk>',views.GetWordcloud,name='wordcloud'),
    path('timeline/<keyword>/<starttime>/<endtime>',views.GetTimeline,name='timeline'),
    path('search/',views.searchNews, name='search'),
    path('search_heatmap/', views.searchNewsWithHeatmap, name='search_hitmap'),
    path('search_date_cluster_info/', views.search_date_cluster_info, name='search_date_cluster_info')
]
