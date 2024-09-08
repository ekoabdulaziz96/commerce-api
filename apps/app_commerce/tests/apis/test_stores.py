from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.app_commerce.tests.factories import StoreFactory


class StoreDetailTest(APITestCase):
    def setUp(self):
        store = StoreFactory()

        self.headers = {"Api-Secret": store.api_secret}
        self.complete_url = reverse("app_commerce:store-detail", args=[store.slug])

    def test_success(self):
        response = self.client.get(self.complete_url, headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
