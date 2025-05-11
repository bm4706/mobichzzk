from django.contrib import admin
from django.urls import path, include
import os
from dotenv import load_dotenv


load_dotenv()  # .env 파일 로드
admin_url = os.environ.get('DJANGO_ADMIN_URL')

urlpatterns = [
    path('admin_url', admin.site.urls),
    path('', include('tracker.urls')),
]
