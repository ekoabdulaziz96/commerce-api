from django.contrib import admin

from apps.app_commerce.models import (
    Channel,
    Delivery,
    Order,
    OrderItem,
    Product,
    Store,
    StoreUser,
)


class StoreAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "api_secret")
    search_fields = ("name",)
    readonly_fields = ("slug",)
    ordering = ["-created_at"]


class StoreUserAdmin(admin.ModelAdmin):
    list_display = ("display_user", "display_store", "display_user_email")
    search_fields = ("store__slug", "user__username", "user__email")
    ordering = ["-created_at"]

    def display_store(self, obj):
        return obj.store

    def display_user(self, obj):
        return obj.user

    def display_user_email(self, obj):
        return obj.user.email

    display_store.short_description = "Store"
    display_user.short_description = "User"
    display_user_email.short_description = "User Email"


class ChannelAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "types", "display_store",)
    search_fields = ("name",)
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def display_store(self, obj):
        return obj.store

    display_store.short_description = "Store"


class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "price", "stock", "display_store")
    search_fields = ("product_id", "name")
    readonly_fields = ("product_id",)
    ordering = ["-created_at"]

    def display_store(self, obj):
        return obj.store

    display_store.short_description = "Store"


class OrderAdmin(admin.ModelAdmin):
    list_display = ( "order_id", "total_amount", "status", "display_channel", "display_store")
    search_fields = ("channel__store__name", "channel__name", "channel__slug", "order_id", "status")
    readonly_fields = ("order_id", "channel", "total_amount")
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def display_store(self, obj):
        return obj.channel.store

    def display_channel(self, obj):
        return obj.channel.slug

    display_store.short_description = "Store"
    display_channel.short_description = "Channel"


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("display_order", "display_product", "quantity", "price")
    search_fields = ("product__name", "order__order_id", "status")
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def display_order(self, obj):
        return obj.order.order_id

    def display_product(self, obj):
        return obj.product.name

    display_order.short_description = "Order"
    display_product.short_description = "Product"


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("display_order", "expedition", "receipt_number", "status", "types")
    search_fields = (
        "order__order_id",
        "expedition",
        "receipt_number",
    )
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def display_order(self, obj):
        return obj.order.order_id

    display_order.short_description = "Order"


admin.site.register(Store, StoreAdmin)
admin.site.register(StoreUser, StoreUserAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Delivery, DeliveryAdmin)
