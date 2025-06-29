import requests

url = "https://api.paymongo.com/v1/checkout_sessions"

payload = { "data": { "attributes": {
            "send_email_receipt": True,
            "show_description": True,
            "show_line_items": True,
            "description": "Monthly subscription to Triple-J Gym.",
            "line_items": [
                {
                    "currency": "PHP",
                    "amount": 100000,
                    "name": "Monthly Subscription",
                    "quantity": 1
                }
            ],
            "payment_method_types": ["qrph", "gcash"]
        } } }
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "authorization": "Basic c2tfdGVzdF9pSkE1cmJlMVJ0Q3BjWmN3TWd6aVVkd3c6"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)