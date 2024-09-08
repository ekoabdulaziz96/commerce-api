from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from apps.app_commerce.models import Order, Product
from apps.app_commerce.paginations import OrderPagination, ProductPagination
from apps.app_commerce.permissions import IsAuthenticatedStore
from apps.app_commerce.serializers.orders import (
    OrderDetailSerializer,
    OrderSerializer,
    ProductBulkUploadSerializer,
    ProductSerializer,
)
from apps.app_commerce.views.stores import MixinStore


class ProductListCreate(generics.ListCreateAPIView, MixinStore):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    ordering = ("-created_at",)
    search_fields = ["name", "slug"]

    def get_queryset(self):
        store = self.get_store()
        return Product.objects.filter(store=store).all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        store = self.get_store()

        serializer = self.get_serializer(data=request.data, context={"request": request, "store": store})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductBulkUpload(generics.CreateAPIView, MixinStore):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = ProductBulkUploadSerializer

    def post(self, request, *args, **kwargs):
        store = self.get_store()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.process(store)

        return Response(data="upload data still in process.", status=status.HTTP_200_OK)


class ProductManage(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = ProductSerializer
    lookup_field = "product_id"
    queryset = Product.objects.all()
    ordering = ("-created_at",)
    search_fields = ["name", "slug"]


class OrderList(generics.ListAPIView, MixinStore):
    permission_classes = [IsAuthenticatedStore]
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    ordering = ("-created_at",)
    search_fields = ["order_id"]

    def get_queryset(self):
        store = self.get_store()
        return Order.objects.filter(channel__store=store).all()


class OrderManage(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedStore]
    lookup_field = "order_id"
    ordering = ("-created_at",)
    search_fields = ["name", "slug"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderDetailSerializer

        return OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(order_id=self.kwargs.get("order_id")).prefetch_related(
            "order_items", "order_deliveries"
        )
        return queryset
