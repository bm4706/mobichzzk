from django.urls import path
from . import views

urlpatterns = [
    path('', views.ranking_list, name='ranking_list'),
    path('crawler/update/secure/', views.run_crawler, name='run_crawler'),
]