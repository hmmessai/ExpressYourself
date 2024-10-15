import time
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('CONSUMER_KEY')
secret = os.getenv('CONSUMER_SECRET')

token_cache = {
    "access_token": None,
    "expires_at": None
}

def get_access_token():
    current_time = time.time() 
    consumer_key = key
    consumer_secret = secret
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    if token_cache["access_token"] and token_cache["expires_at"] > current_time:
        return token_cache["access_token"] 

    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    new_token = response.json().get("access_token")
    expires_in = response.json().get("expires_in", 3600)

    token_cache["access_token"] = new_token
    token_cache["expires_at"] = current_time + float(expires_in) - 10

    return new_token

def send_payment_request(token, amount):
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    payload = {
        "BusinessShortCode": "174379",
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQxMDEzMjIxMjE0",
        "Timestamp": "20241013221214",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": "254708374149",
        "PartyB": "174379",
        "PhoneNumber": "254708374149",
        "CallBackURL": "http://127.0.0.1:8000/process_payment",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
    }

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload)
    print(response.text.encode('utf8'))