from django.urls import path, include
from .views import cctv_page

app_name = 'cctv_page'		# 네임 스페이스

urlpatterns = [
    path("", cctv_page),
]
