from django.conf import settings
from requests import request


class AppChannelException(BaseException):
    pass

class AppChannel():
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Api-Secret": settings.APP_CHANNEL_API_SECRET
        }
        self.base_url = settings.APP_CAHNNEL_BASE_URL

    def _do_request(self):
        try:
            response = request(method=self.method, url=self.url, json=self.data, headers=self.headers)
            if response.status_code >= 400:
                raise AppChannelException("error: ", response.content)

            print(response.json())
            return response.json()

        except Exception as err:
            raise(err)

    def sync_store(self, obj):
        self.method = "POST"
        self.url = self.base_url + "/api/v1/channels/sync-store/"
        self.data = {
            "name": obj.name,
            "slug": obj.slug,
            "api_secret": obj.api_secret
        }

        return self._do_request()

    def sync_product_stock(self, obj):
        self.method = "POST"
        self.url = self.base_url + "/api/v1/channels/sync-stock/"
        self.data = {
            "product_id": str(obj.product_id),
            "name": obj.name,
            "stock": obj.stock
        }
        return self._do_request()

    def sync_order_status(self, data):
        self.method = "POST"
        self.url = self.base_url + "/api/v1/channels/sync-order/status/"
        self.data = data
        return self._do_request()


app_channel = AppChannel()
