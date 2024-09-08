from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from apps.app_commerce.models import Store


class IsAuthenticatedStore(BasePermission):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        api_secret = request.headers.get("Api-Secret", None)
        slug = request.parser_context.get("kwargs", {}).get("slug", None)

        return Store.objects.filter(slug=slug, api_secret=api_secret).exists()

class IsAuthenticatedAppChannel(BasePermission):
    message = PermissionDenied.default_detail

    def has_permission(self, request, view):
        api_secret = request.headers.get("Api-Secret", None)

        return api_secret == settings.API_SECRET_APP_CHANNEL
