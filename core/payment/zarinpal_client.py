from django.conf import settings

import json
import requests

class ZarinPal:
    _request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
    _verify_url = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
    _payment_url = 'https://sandbox.zarinpal.com/pg/StartPay/'
    _callback_url = 'http://127.0.0.1:8000/payment/verify'

    def __init__(self):
        self.merchant_id = settings.MERCHANT_ID

    def post_payment_request(self, amount, description='Successful payment!'):
        data = {
            "merchant_id": self.merchant_id,
            "amount": str(amount),
            "callback_url": self._callback_url,
            "referrer_id": "xxxx",
            "description": description
        }
        response = requests.post(
            self._request_url,
            headers={'content-type': 'application/json'},
            data=json.dumps(data)
        )
        return response.json()

    def post_payment_verify(self, amount, authority):
        data = {
            "merchant_id": self.merchant_id,
            "amount": str(amount),
            "authority": authority
        }
        response = requests.post(
            self._verify_url,
            headers={'content-type': 'application/json'},
            data=json.dumps(data)
        )
        return response.json()

    def generate_payment_url(self, authority):
        return self._payment_url + authority
    