from django.urls import path
from . import views
import os
from dotenv import load_dotenv

load_dotenv()

crawler_url = os.environ.get('DJANGO_CRAWLER_URL')  

urlpatterns = [
    path('', views.ranking_list, name='ranking_list'),
    path(crawler_url, views.run_crawler, name='run_crawler'),
]