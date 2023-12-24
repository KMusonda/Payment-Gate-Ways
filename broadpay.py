import requests
import json
import uuid
import jwt

class BroadPay:
    merchant_public_key = "your pub key"
    merchant_secret_key = "your secrete key"

    @staticmethod
    def request_pay(amount, transaction_id, first_name, last_name, email_address, phone_number):
        #the transaction_id of the order model is the same as the transactionReference

        url = 'https://checkout.broadpay.io/gateway/api/v1/checkout'
        headers = {'Content-Type': 'application/json'}
        data = {
            "transactionName": "transaction_name",
            "amount": amount,
            "currency": "ZMW",
            "transactionReference": transaction_id,
            "customerFirstName": first_name,
            "customerLastName": last_name,
            "customerEmail": email_address,
            "customerPhone": phone_number,
            "returnUrl": f"http://127.0.0.1:8000/cart/success/{transaction_id}",
            "autoReturn": True,
            "merchantPublicKey": BroadPay.merchant_public_key
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result

    @staticmethod
    def verify_transaction(reference):
        url = f'https://live.broadpay.io/gateway/api/v1/transaction/query?reference={reference}'

        payload = {
            "pubKey": BroadPay.merchant_public_key
        }

        #create a jwt token
        jwt_token = jwt.encode(payload, BroadPay.merchant_secret_key, algorithm='HS256')        

        headers = {'token': jwt_token}

        response = requests.get(url, headers=headers)
        result = response.json()

        return result