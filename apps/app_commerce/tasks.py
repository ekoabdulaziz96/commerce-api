from celery import shared_task

from apps.app_commerce.models import Product, Store


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
