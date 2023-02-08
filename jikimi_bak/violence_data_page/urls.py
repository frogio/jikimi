from django.urls import path
from .views import violence_data_page

app_name = 'violence_data_page'		# 네임 스페이스

urlpatterns = [
    path("", violence_data_page, name="violence_data_page"),
]
