from django.conf.urls import include
from django.urls import path

from apps.app_commerce.urls import v1

app_name = "app_commerce"

urlpatterns = [
    path("api/v1/commerce/", include(v1)),
]
