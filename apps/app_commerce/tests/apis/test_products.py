from unittest import mock
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.app_commerce.tests.factories import ProductFactory, StoreFactory


class ProductListTest(APITestCase):
    @mock.patch("apps.modules.app_channels.AppChannel._do_request", return_value="ok")
    def setUp(self, _):
        self.store = StoreFactory()
        ProductFactory.create_batch(5, store=self.store)

        self.headers = {"Api-Secret": self.store.api_secret}
        self.complete_url = reverse("app_commerce:product-list-create", args=[self.store.slug])

    def test_success(self):
        response = self.client.get(self.complete_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(len(response.data["results"][0]), 5)


class ProductCreateTest(APITestCase):
    @mock.patch("apps.modules.app_channels.AppChannel._do_request", return_value="ok")
    def setUp(self, _):
        self.store = StoreFactory()

        self.headers = {"Api-Secret": self.store.api_secret}
        self.complete_url = reverse("app_commerce:product-list-create", args=[self.store.slug])
        self.payload = {"name": "Product Unittest", "description": "like new", "price": 10000, "stock": 50}

    @mock.patch("apps.modules.app_channels.AppChannel._do_request", return_value="ok")
    def test_success(self, _):
        response = self.client.post(self.complete_url, data=self.payload, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data["name"], "Product Unittest")


class ProductDetailTest(APITestCase):
    @mock.patch("apps.modules.app_channels.AppChannel._do_request", return_value="ok")
    def setUp(self, _):
        self.store = StoreFactory()
        self.product = ProductFactory(store=self.store, name="Product Unittest Detail")

        self.headers = {"Api-Secret": self.store.api_secret}
        self.complete_url = reverse("app_commerce:product-manage", args=[self.store.slug, self.product.product_id])

    def test_success(self):
        response = self.client.get(self.complete_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data["name"], "Product Unittest Detail")


class ProductUpdateTest(APITestCase):
    @mock.patch("apps.modules.app_channels.AppChannel._do_request", return_value="ok")
    def setUp(self, _):
        self.store = StoreFactory()
        self.product = ProductFactory(store=self.store)

        self.headers = {"Api-Secret": self.store.api_secret}
        self.complete_url = reverse("app_commerce:product-manage", args=[self.store.slug, self.product.product_id])
        self.payload = {"name": "Product Unittest Updated", "description": "like new", "price": 10000, "stock": 50}

    @mock.patch("apps.modules.app_channels.AppChannel._do_request", return_value="ok")
    def test_success(self, _):
        response = self.client.patch(self.complete_url, data=self.payload, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data["name"], "Product Unittest Updated")
