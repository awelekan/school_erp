import requests
from django.conf import settings

class PaymentGateway:
    @staticmethod
    def initialize_payment(amount, email, payment_method):
        if payment_method == "paystack":
            url = "https://api.paystack.co/transaction/initialize"
            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            }
            data = {"email": email, "amount": int(amount * 100)}
            response = requests.post(url, json=data, headers=headers)
            return response.json()

        elif payment_method == "flutterwave":
            url = "https://api.flutterwave.com/v3/payments"
            headers = {
                "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                "Content-Type": "application/json",
            }
            data = {"tx_ref": "FLW" + str(amount), "amount": amount, "currency": "NGN", "redirect_url": settings.FRONTEND_URL}
            response = requests.post(url, json=data, headers=headers)
            return response.json()

        return None

    @staticmethod
    def verify_payment(payment_method, reference):
        if payment_method == "paystack":
            url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
            response = requests.get(url, headers=headers)
            return response.json()

        elif payment_method == "flutterwave":
            url = f"https://api.flutterwave.com/v3/transactions/{reference}/verify"
            headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}
            response = requests.get(url, headers=headers)
            return response.json()

        return None
