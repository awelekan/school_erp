import requests
from django.conf import settings

PAYSTACK_SECRET_KEY = "your_paystack_secret_key"
FLUTTERWAVE_SECRET_KEY = "your_flutterwave_secret_key"

def initialize_paystack_payment(amount, email):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {"email": email, "amount": int(amount * 100)}  # Convert to kobo
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def verify_paystack_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

def initialize_flutterwave_payment(amount, email):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "tx_ref": "TX-" + str(amount) + "-REF",
        "amount": amount,
        "currency": "NGN",
        "redirect_url": "https://yourfrontend.com/payment-success",
        "customer": {"email": email},
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def verify_flutterwave_payment(transaction_id):
    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {"Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()
