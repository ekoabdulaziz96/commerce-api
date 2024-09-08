from django.urls import path

from apps.app_commerce.views import orders, stores

urlpatterns = [
    path("stores/<str:slug>/", stores.StoreDetail.as_view(), name="store-detail"),
    path("sync-channel/", stores.ChannelSync.as_view(), name="channel-sync"),

    path("stores/<str:slug>/products/", orders.ProductListCreate.as_view(), name="product-list-create"),
    path("stores/<str:slug>/products/bulk-upload", orders.ProductBulkUpload.as_view(), name="product-bulk-upload"),
    path("stores/<str:slug>/products/<uuid:product_id>", orders.ProductManage.as_view(), name="product-manage"),

    path("stores/<str:slug>/orders/", orders.OrderList.as_view(), name="order-list"),
    path("stores/<str:slug>/orders/<str:order_id>/", orders.OrderManage.as_view(), name="order-manage"),
]
