from factory import Faker, fuzzy, LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory

from apps.app_commerce.models import Channel, Delivery, Order, OrderItem, Product, Store
from apps.bases.utils import create_slug


class StoreFactory(DjangoModelFactory):
    name = Faker("name")
    slug = LazyAttribute(lambda obj: create_slug(obj.name, Store))
    api_secret = Sequence(lambda n: "api_secret" + str(n))

    class Meta:
        model = Store


class ChannelFactory(DjangoModelFactory):
    store = SubFactory(StoreFactory)
    name = Faker("name")
    slug = LazyAttribute(lambda obj: create_slug(obj.name, Channel))
    types = "marketplace"

    class Meta:
        model = Channel


class ProductFactory(DjangoModelFactory):
    store = SubFactory(StoreFactory)
    name = Faker("name")
    description = Faker("sentence")
    price = fuzzy.FuzzyChoice(choices=[price for price in (1000,1000000, 500)])
    stock = fuzzy.FuzzyChoice(choices=[price for price in (10,100)])

    class Meta:
        model = Product


class OrderFactory(DjangoModelFactory):
    channel = SubFactory(ChannelFactory)
    order_id = Sequence(lambda n: "order_id_" + str(n))
    total_amount = 1000000
    status = "pending"

    class Meta:
        model = Order


class OrderItemFactory(DjangoModelFactory):
    order = SubFactory(OrderFactory)
    product = SubFactory(ProductFactory)
    quantity = 1
    price = 1000

    class Meta:
        model = OrderItem


class DeliveryFactory(DjangoModelFactory):
    order = SubFactory(OrderFactory)
    types = "purchase"
    expedition = Faker("name")
    receipt_number = Sequence(lambda n: "receipt_" + str(n))
    address = "random"
    status = "transit"

    class Meta:
        model = Delivery

