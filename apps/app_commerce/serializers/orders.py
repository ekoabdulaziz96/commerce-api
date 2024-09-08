import codecs
import csv

from rest_framework import serializers

from apps.app_commerce import settings as app_settings
from apps.app_commerce.models import Delivery, Order, OrderItem, Product
from apps.app_commerce.serializers.stores import ChannelSerializer
from apps.app_commerce.tasks import product_bulk_upload_task
from apps.bases.serializers import BaseModelSerializer, BaseSerializer, ChoiceDisplayField


class ProductSerializer(BaseModelSerializer):
    product_id = serializers.CharField(read_only=True)
    stock = serializers.IntegerField(required=True, min_value=0)

    class Meta:
        model = Product
        fields = ["product_id", "name", "description", "price", "stock"]

    def save(self, **kwargs):
        if not self.instance:
            self.validated_data["store"] = self.context["store"]

        return super().save(**kwargs)


class SimpleProductSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ["product_id", "name", "description"]


class ProductBulkUploadSerializer(BaseSerializer):
    csv_file = serializers.FileField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        csv_file = data.pop("csv_file")
        if csv_file.content_type != "text/csv":
            raise serializers.ValidationError({"csv_file": app_settings.MSG_PRODUCT_INVALID_FILE_FORMAT})

        products = csv.reader(codecs.iterdecode(csv_file, "utf-8"), delimiter=",")
        next(products)

        products = list(products)
        if len(products[0]) != 4:
            raise serializers.ValidationError({"csv_file": app_settings.MSG_PRODUCT_INVALID_FILE_DATA})

        data["products"] = products
        return data

    def process(self, store):
        product_bulk_upload_task.delay(store.id, self.validated_data["products"])


class OrderItemSerializer(BaseModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class DeliverySerializer(BaseModelSerializer):
    types = ChoiceDisplayField(choices=Delivery.TYPE_CHOICES)

    class Meta:
        model = Delivery
        fields = ["expedition", "receipt_number", "address", "status", "types"]


class OrderSerializer(BaseModelSerializer):
    channel_slug = serializers.CharField(read_only=True, source="channel.slug")
    status = ChoiceDisplayField(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ["channel_slug", "order_id", "total_amount", "status"]
        read_only_fields = ["channel_slug", "order_id", "total_amount", "status"]

    def save(self, **kwargs):
        if self.instance and self.instance.status == "pending" and self.validated_data["status"] == "processing":
            print("trigger app channel to update status and wait for escpedition data")

        return super().save(**kwargs)


class OrderDetailSerializer(BaseModelSerializer):
    channel = ChannelSerializer()
    status = ChoiceDisplayField(choices=Order.STATUS_CHOICES)
    items = OrderItemSerializer(source="order_items", many=True)
    deliveries = DeliverySerializer(source="order_deliveries", many=True)

    class Meta:
        model = Order
        fields = ["channel", "items", "deliveries", "order_id", "total_amount", "status"]
