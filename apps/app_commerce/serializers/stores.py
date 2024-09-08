from itertools import chain

from rest_framework import serializers

from apps.app_commerce import settings as app_settings
from apps.app_commerce.models import Channel, Store
from apps.bases.serializers import BaseModelSerializer, BaseSerializer, ChoiceDisplayField


class MyStoreSerializer(BaseModelSerializer):
    slug = serializers.CharField(read_only=True)
    api_secret = serializers.CharField(read_only=True)

    class Meta:
        model = Store
        fields = ["name", "slug", "api_secret"]


class StoreSerializer(MyStoreSerializer):

    class Meta:
        model = Store
        fields = ["name", "slug"]


class ChannelSerializer(BaseModelSerializer):
    store = StoreSerializer()
    types = ChoiceDisplayField(choices=Channel.TYPE_CHOICES)

    class Meta:
        model = Channel
        fields = ["store", "slug", "name", "types"]


class ChannelSyncSerializer(BaseSerializer):
    store_slug = serializers.CharField(required=True)
    slug = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    types = serializers.CharField(required=True)

    class Meta:
        fields = ["store_slug", "slug", "name", "types"]

    def validate(self, attrs):
        data = super().validate(attrs)
        store = Store.objects.filter(slug=data.pop("store_slug")).first()
        if not store:
            raise serializers.ValidationError({"store_slug": app_settings.MSG_STORE_NOT_FOUND})

        if data["types"] not in list(chain(*Channel.TYPE_CHOICES)):
            raise serializers.ValidationError({"types": app_settings.MSG_CHANNEL_TYPE_NOT_FOUND})

        data["store"] = store
        return data

    def save(self, **kwargs):
        store = self.validated_data.pop("store")
        slug = self.validated_data.pop("slug")
        channel, created = Channel.objects.get_or_create(store=store, slug=slug, defaults=self.validated_data)
        if not created:
            channel.name = self.validated_data["name"]
            channel.types = self.validated_data["types"]
            channel.save()

        return ChannelSerializer(channel).data
