from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.app_commerce.tests.factories import (
    ChannelFactory,
    DeliveryFactory,
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    StoreFactory,
)


class OrderListTest(APITestCase):
    def setUp(self):
        self.store = StoreFactory()
        self.channel = ChannelFactory(store=self.store)
        OrderFactory.create_batch(5, channel=self.channel)

        self.headers = {"Api-Secret": self.store.api_secret}
        self.complete_url = reverse("app_commerce:order-list", args=[self.store.slug])

    def test_success(self):
        response = self.client.get(self.complete_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(len(response.data["results"][0]), 4)


class OrderDetailTest(APITestCase):
    def setUp(self):
        self.store = StoreFactory()
        self.channel = ChannelFactory(store=self.store)
        self.order = OrderFactory(channel=self.channel)

        self.headers = {"Api-Secret": self.store.api_secret}
        self.complete_url = reverse("app_commerce:order-manage", args=[self.store.slug, self.order.order_id])

    def test_success(self):
        products = ProductFactory.create_batch(2, store=self.store)
        OrderItemFactory(product=products[0], order=self.order)
        OrderItemFactory(product=products[1], order=self.order)
        DeliveryFactory(order=self.order)

        response = self.client.get(self.complete_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(len(response.data["deliveries"]), 1)


class OrderProcessTest(APITestCase):
    def setUp(self):
        self.store = StoreFactory()
        self.channel = ChannelFactory(store=self.store)
        self.order = OrderFactory(channel=self.channel)

        self.headers = {"Api-Secret": self.store.api_secret}
        self.complete_url = reverse("app_commerce:order-manage", args=[self.store.slug, self.order.order_id])
        self.payload = {"status": "processing"}

    def test_success(self):
        products = ProductFactory.create_batch(2, store=self.store)
        OrderItemFactory(product=products[0], order=self.order)
        OrderItemFactory(product=products[1], order=self.order)
        DeliveryFactory(order=self.order)

        response = self.client.patch(self.complete_url, data=self.payload, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["status"]["value"], "processing")
