from django.urls import path
from .views import signup, my_page, uploadProfileImages, UserLoginView
from django.contrib.auth import views as auth_views

app_name = 'account'		# 네임 스페이스

urlpatterns = [
    path("login/", UserLoginView.as_view(template_name = "account/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path("my_page/", my_page ,name="mypage"),
    path('upload-prop-images/', uploadProfileImages, name='profile_img'),
]
