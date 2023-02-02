from django.urls import path
from .views import cctv_page

app_name = 'cctv_page'		# 네임 스페이스

urlpatterns = [
    path("", cctv_page, name="cctv_page"),
]
