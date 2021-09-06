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
from qleader.views import (compare_detail, result_receiver, detail, delete_result,
                           home, leaderboard, invoke_leaderboard, get_token,
                           change_publicity, get_leaderboard_distances,
                           download_result, profile, modify_info, modify_profile,
                           user_logout, get_fci_values)
from django.urls import path, include, re_path
# from django.contrib import admin


urlpatterns = [
    path('api/<int:result_id>/', detail),
    path('api/<int:result_id>/delete/', delete_result),
    path('api/<int:result_id>/change_publicity/', change_publicity),
    path('api/<int:result_id>/download/<str:type>/', download_result),
    path('api/<int:result_id>/modify_info/', modify_info),
    path('api/distances/', get_leaderboard_distances),
    path('api/fci/<str:basis_set>/', get_fci_values),
    path('api/', result_receiver),
    path('leaderboard/', leaderboard),
    path('leaderboard/<str:criterion>/', invoke_leaderboard, name='invoke_leaderboard'),
    path('api/compare/', compare_detail),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/logout/', user_logout),
    re_path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user/<int:user_id>/', profile),
    path('user/<int:user_id>/modify_profile/', modify_profile),
    path('get-token/', get_token),
    # path('admin/', admin.site.urls),
    path('', home),
]
