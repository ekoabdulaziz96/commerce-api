from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.app_commerce import settings as app_settings
from apps.app_commerce.models import Store
from apps.app_commerce.permissions import IsAuthenticatedAppChannel, IsAuthenticatedStore
from apps.app_commerce.serializers.stores import ChannelSyncSerializer, MyStoreSerializer


class MixinStore():
    def get_store(self):
        store = Store.objects.filter(slug=self.kwargs["slug"]).first()
        if not store:
            raise NotFound(app_settings.MSG_STORE_NOT_FOUND)

        return store


class StoreDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = MyStoreSerializer
    queryset = Store.objects.all()
    lookup_field = "slug"


class ChannelSync(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedAppChannel]
    serializer_class = ChannelSyncSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=status.HTTP_200_OK)

