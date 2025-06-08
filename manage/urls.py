"""
URL configuration for manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from system.views import LoginView, LogoutView, CaptchaImageView, RoutersView
from system.user.views import LoginUserInfoView


urlpatterns = [
    #path("admin/", admin.site.urls),
    path('login', LoginView.as_view(), name='login'), # 登录
    path('logout', LogoutView.as_view(), name="logout"), # 登出
    path('getInfo', LoginUserInfoView.as_view(), name='getInfo'), # 获取用户信息
    path('captchaImage', CaptchaImageView.as_view(), name='captchaImage'), # 验证码
    path('getRouters', RoutersView.as_view(), name='getRouters'), # 路由
    path('system/', include('system.urls')), # 系统模块
    path('monitor/', include('monitor.urls')), # 监控模块
    path('tool/gen/', include('generator.urls')), # 代码生成工具

]
