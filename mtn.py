#payment with mtn mobile money
from base64 import encode
import json
import uuid
from django.conf import settings
import requests


class PayClass():
    collections_subkey = settings.MTN_SUBSCRIPTION_KEY    
    basic_authorisation_collections = ""    
    collections_apiuser = ""
    api_key_collections = ""    
    environment_mode = "sandbox"
    accurl = "https://proxy.momoapi.mtn.com"

    if environment_mode == "sandbox":
        accurl = "https://sandbox.momodeveloper.mtn.com"

    if environment_mode == "sandbox":
        currency = 'EUR'
    else:
        currency = 'ZMW'

    if environment_mode == "sandbox":
        collections_apiuser = str(uuid.uuid4())        

    url = f"{accurl}/v1_0/apiuser" #call back for collections
    payload = json.dumps({
        "providerCallbackHost": "URL of host ie google.com"
    })
    headers = {
        'X-Reference-Id': collections_apiuser,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': collections_subkey
    }
    response = requests.post(url, headers=headers, data=payload)

    url = f"{accurl}/v1_0/apiuser/{collections_apiuser}/apikey"
    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': collections_subkey
    }
    response = requests.post(url, headers=headers, data=payload)
    response = response.json()

    if environment_mode == "sandbox":
        api_key_collections = str(response["apiKey"])

    username, password = collections_apiuser, api_key_collections
    basic_authorisation_collections = encode(username, password)

    def momotoken(self):
        url = f"{PayClass.accurl}/collection/token/"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Authorization': str(PayClass.basic_authorisation_collections)
        }
        response = requests.post(url, headers=headers, data=payload)
        authorization_token = response.json()
        return authorization_token

    def momopay(self, amount, currency, txt_ref, phone_number, payermessage):
        uuidgen = str(uuid.uuid4())
        url = f"{PayClass.accurl}/collection/v1_0/requesttopay"
        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "externalId": txt_ref,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": payermessage,
            "payeeNote": payermessage
        })
        headers = {
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': PayClass.environment_mode,
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {str(PayClass.momotoken(self)['access_token'])}"
        }
        response = requests.post(url, headers=headers, data=payload)
        context = {"response": response.status_code, "ref": uuidgen}
        return context

    def verifymomo(self, txn):
        url = f"{PayClass.accurl}/collection/v1_0/requesttopay/{str(txn)}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Authorization': f"Bearer {str(PayClass.momotoken(self)['access_token'])}",
            'X-Target-Environment': PayClass.environment_mode,
        }
        response = requests.get(url, headers=headers, data=payload)
        json_response = response.json()
        return json_response

    def momobalance(self):
        url = f"{PayClass.accurl}/collection/v1_0/account/balance"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Authorization': f"Bearer {str(PayClass.momotoken(self)['access_token'])}",
            'X-Target-Environment': PayClass.environment_mode,
        }
        response = requests.get(url, headers=headers, data=payload)
        json_response = response.json()
        return json_response 