import uuid
import requests
import json

class PayWithPayPesapal:
    def __init__(self):
        self.environment_mode = "sandbox"
        self.access_token = None
        if self.environment_mode == "sandbox":
            self.consumer_key = "v988cq7bMB6AjktYo/drFpe6k2r/y7z3"
            self.consumer_secret = "3p0F/KcY8WAi36LntpPf/Ss0MhQ="
            self.callback_url = "http://127.0.0.1:8000/cart/success"
            self.notification = "https://http://127.0.0.1:8000/pesapal/notification"
        else:
            self.consumer_key = "your pub key"
            self.consumer_secret = "your secrete key"
            self.callback_url = "https://example.com/success"
            self.notification = "https://example.com/notification"
        self.id = str(uuid.uuid4())
    
    def generate_access_token(self):
        try:
            if self.environment_mode == "sandbox":
                url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
            else:
                url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"

            payload = json.dumps({
                "consumer_key": self.consumer_key,
                "consumer_secret": self.consumer_secret,
            })

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }

            response = requests.post(url, headers=headers, data=payload)
            access_token = response.json().get('token')
            if response.status_code == 200:
                self.access_token = access_token
            return access_token if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Failed to generate access token: {e}")
            return None
        
    def get_access_token(self):
        if not self.access_token:
            self.access_token = self.generate_access_token()
        return self.access_token

    def register_ipn_and_extract_id(self, access_token):
        try:
            if self.environment_mode == "sandbox":
                url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"
            else:
                url = "https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN"

            payload = json.dumps({
                "url": self.notification,
                "ipn_notification_type": "GET"
            })
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {access_token}",
            }

            response = requests.post(url, headers=headers, data=payload)
            response_data = response.json()
            ipn_id = response_data.get('ipn_id')
            return ipn_id
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def paysapal_payment_request(self, amount, email_address, phone_number, first_name, last_name):
        access_token = self.get_access_token()

        if access_token:
            notification_id = self.register_ipn_and_extract_id(access_token)

            if notification_id:
                try:
                    if self.environment_mode == "sandbox":
                        url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"
                    else:
                        url = "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest"

                    payload = json.dumps({
                        "id": self.id,
                        "currency": "ZMW",
                        "amount": amount,
                        "description": "Payment description goes here",
                        "callback_url": self.callback_url,
                        "notification_id": notification_id,
                        "billing_address": {
                            "email_address": email_address,
                            "phone_number": phone_number,
                            "country_code": "ZM",
                            "first_name": first_name,
                            "last_name": last_name,
                        }
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f"Bearer {access_token}",
                    }

                    response = requests.post(url, headers=headers, data=payload)
                    payment_response = response.json()
                    order_tracking_id = payment_response.get("order_tracking_id")
                    redirect_url = payment_response.get("redirect_url")
                    return {"order_tracking_id": order_tracking_id, "redirect_url": redirect_url}
                except requests.RequestException as e:
                    print(f"Request failed: {e}")
                    return {"order_tracking_id": None, "redirect_url": None}
            else:
                print("Failed to obtain notification_id")
                return {"order_tracking_id": None, "redirect_url": None}
        else:
            print("Failed to obtain access token")
            return {"order_tracking_id": None, "redirect_url": None}
        
    def get_transaction_status(self, order_tracking_id):
        access_token = self.get_access_token()
        
        if access_token:
            try:
                if self.environment_mode == "sandbox":
                    url = f"https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}"
                else:
                    url = f"https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}"  # Use orderTrackingId in URL
                
                payload = {}
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f"Bearer {access_token}"
                }

                response = requests.get(url, headers=headers, data=payload)
                json_response = response.json()
                #response_status = json_response.get("status")
                return json_response                
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                return None
        else:
            print("Failed to obtain access token")
            return None
