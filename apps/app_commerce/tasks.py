from celery import shared_task
from django.db import transaction

from apps.app_commerce.models import Channel, Order, OrderItem, Product, Store


@shared_task
def product_bulk_upload_task(store_pk, products):
    store = Store.objects.get(pk=store_pk)
    chunk_size = 100
    chunk_products = [products[i : i + chunk_size] for i in range(0, len(products), chunk_size)]

    for chunk_item_products in chunk_products:
        Product.objects.bulk_create(
            [
                Product(
                    store=store,
                    name=product[0],
                    description=product[1],
                    price=product[2],
                    stock=product[3],
                )
                for product in chunk_item_products
            ]
        )

    return "success"


@shared_task
@transaction.atomic
def open_order_task(orders):
    channel = Channel.objects.filter(slug=orders["channel_slug"]).first()
    order, _ = Order.objects.get_or_create(
        channel=channel, order_id=orders["order_id"], defaults={"status": "open", "total_amount": 0}
    )

    items = orders.pop("items")
    total_amount = 0
    for item in items:
        total_amount += item.pop("total_price")
        product = Product.objects.filter(product_id=item["product_id"]).first()
        OrderItem(
            order=order,
            product=product,
            quantity=item["quantity"],
            price=item["price"],
        ).save()

        product.stock -= item["quantity"]
        product.save()

    order.total_amount = total_amount
    order.save()
