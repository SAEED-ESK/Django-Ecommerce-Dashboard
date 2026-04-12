import json
import requests

class ZarinPal:
    _request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
    _verify_url = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
    _payment_url = 'https://sandbox.zarinpal.com/pg/StartPay/'
    _callback_url = 'http://127.0.0.1:8000/verify'

    def __init__(self, merchant_id):
        self.merchant_id = merchant_id

    def post_payment_request(self, amount, description='Successful payment!'):
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": self._callback_url,
            "referrer_id": "xxxx",
            "description": description,
            "metadata": {"mobile": "09121234567","email": "info.test@gmail.com"}
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
            "amount": amount,
            "authority": authority
        }
        response = requests.post(
            self._request_url,
            headers={'content-type': 'application/json'},
            data=json.dumps(data)
        )
        return response.json()

    def generate_payment_url(self, authority):
        return self._payment_url + authority
    
if __name__ == '__main__':
    zarinpal = ZarinPal('550e8400-e29b-41d4-a716-446655440000')
    response = zarinpal.post_payment_request(15000)
    print(response)
    authority = response['data']['authority']
    print(authority)
    input("proceed to generating payment url?")
    print(zarinpal.generate_payment_url(authority))
    input("check the payment?")
    response = zarinpal.post_payment_verify(15000, authority)
    print(response)