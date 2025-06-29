import requests

url = "https://api.paymongo.com/v1/webhooks"

payload = { "data": { "attributes": {
            "url": "https://triple-j.onrender.com/api/account/membership/successful",
            "events": ["checkout_session.payment.paid"]
        } } }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic c2tfdGVzdF9pSkE1cmJlMVJ0Q3BjWmN3TWd6aVVkd3c6"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)