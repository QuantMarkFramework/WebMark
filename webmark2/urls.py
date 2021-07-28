"""webmark2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
# from django.shortcuts import redirect
# from django.views.generic.base import RedirectView
from qleader.views import (compare_detail, result_list, detail,
                           home, leaderboard, invoke_leaderboard)
from django.urls import path, include, re_path
from django.contrib import admin
# from webmark2.settings import ROOT_DIR

urlpatterns = [
    path('api/<int:result_id>/', detail),
    path('api/', result_list),
    path('leaderboard/', leaderboard),
    path('leaderboard/<str:criterion>/', invoke_leaderboard, name='invoke_leaderboard'),
    path('api/compare/', compare_detail),
    re_path('', include('social_django.urls', namespace='social')),
    re_path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', home),
]
