from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("jwt/create/", jwt_views.TokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", jwt_views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", jwt_views.TokenVerifyView.as_view(), name="jwt-verify"),
]
