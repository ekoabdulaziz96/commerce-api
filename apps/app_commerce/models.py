from uuid import uuid4

from django.db import models

from apps.app_users.models import User
from apps.bases.models import BaseModel, SafeDeleteModel
from apps.bases.utils import create_slug


class Store(SafeDeleteModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    api_secret = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "app_commerce_stores"

    def __str__(self):
        return self.slug

    def __init__(self, *args, **kwargs):
        super(Store, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, keep_deleted=False, **kwargs):
        if not self.pk or self.__original_name != self.name:
            self.slug = create_slug(self.name, Store)

        # from apps.bases.auths import auth_api_secret
        # if not self.api_secret:
        #     self.api_secret = auth_api_secret.generate(str(self.slug))

        return super().save(keep_deleted, **kwargs)


class StoreUser(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_users")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="store_user")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "app_commerce_store_users"
        unique_together = ("store", "user")


class Channel(SafeDeleteModel):
    TYPE_CHOICES = (
        ("marketplace", "Marketplace"),
        ("shopify", "Shopify"),
        ("pos", "POS"),
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_channels")
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    types = models.CharField(max_length=50, choices=TYPE_CHOICES)

    class Meta:
        db_table = "app_commerce_channels"


class Product(SafeDeleteModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="store_products")
    product_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "app_commerce_products"


class Order(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
        ("refund", "Refund"),
    ]
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel_orders")
    order_id = models.CharField(max_length=125, unique=True)  # from order number in specific channel
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    class Meta:
        db_table = "app_commerce_orders"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "app_commerce_order_items"


class Delivery(BaseModel):
    TYPE_CHOICES = (
        ("purchase", "Purchase"),
        ("refund", "Refund"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_deliveries")
    types = models.CharField(max_length=50, choices=TYPE_CHOICES)
    expedition = models.CharField(max_length=75)
    receipt_number = models.CharField(max_length=125)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100)  # based on expedition

    class Meta:
        db_table = "app_commerce_order_deliveries"
