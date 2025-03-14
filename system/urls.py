from tkinter.font import names

from django.urls import path

from system.views import LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'), # 登录
]