from django.test.utils import override_settings
from unittest import mock
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.app_commerce.tests.factories import StoreFactory


class ChannelSyncTest(APITestCase):
    @mock.patch("apps.modules.app_channels.AppChannel._do_request", return_value="ok")
    def setUp(self, _):
        self.store = StoreFactory()

        self.headers = {"Api-Secret": settings.APP_COMMERCE_API_SECRET}
        self.complete_url = reverse("app_commerce:channel-sync")
        self.payload = {
            "store_slug": self.store.slug,
            "slug": "test_sync_marketplace",
            "name": "test sync marketplace",
            "types": "marketplace",
        }

    def test_success(self):
        response = self.client.post(self.complete_url, data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data["store"]), 2)

        with self.subTest("check update for exist channel"):
            self.payload["name"] = "updated"
            response = self.client.post(self.complete_url, data=self.payload, headers=self.headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            self.assertEqual(len(response.data["store"]), 2)
            self.assertEqual(response.data["name"], "updated")
