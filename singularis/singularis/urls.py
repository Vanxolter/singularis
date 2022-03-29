"""singularis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from history.views import my_history, delete_place, delete_route, jesus_eyes
from main.views import showmap
from transports.views import airplane, auto
from users.views import authorization, logout_view, register

urlpatterns = [
    path("admin/django-rq/", include("django_rq.urls")),
    path("admin/", admin.site.urls),

    path("login/", authorization, name="login"),  # АВТОРИЗАЦИЯ
    path("register/", register, name="register"),  # РЕГИСТРАЦИЯ
    #path("register/", SignUpView.as_view(), name="register"),  # РЕГИСТРАЦИЯ через класс
    path("logouthtml/", logout_view, name="logout"),  # ВЫХОД ИЗ ПРОФИЛЯ

    path("history/", my_history, name="history"),  # ИСТОРИЯ ПОИСКА
    path("delete/<int:place_id>/", delete_place, name="delete_place"),  # УДАЛЕНИЕ МЕСТА
    path("delete/<int:route_id>/", delete_route, name="delete_route"),  # УДАЛЕНИЕ МАРШРУТА
    path("jesus_eyes/", jesus_eyes, name="jesus_eyes"),  # Визуализация истории

    path('<str:lat1>,<str:long1>,<str:lat2>,<str:long2>', airplane, name='fly'), # САМОЛЕТ
    path('<str:lat1>,<str:long1>,<str:lat2>,<str:long2>', auto, name='auto'),  # АВТО
    path("", showmap, name='home'), # ДОМАШНЯЯ СТРАНИЦА
]