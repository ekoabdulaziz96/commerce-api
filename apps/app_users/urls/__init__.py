from django.conf.urls import include
from django.urls import path

from apps.app_users.urls import users

app_name = "app_users"
urlpatterns = [
    path("", include(users)),
]
