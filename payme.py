from broadpay import BroadPay  # Assuming the class is in a file named broadpay.py

# Instantiate the BroadPay class
pay = BroadPay()

# Use the payment_request method
payment_response = pay.request_pay(
    amount=100,
    email_address="kanyantamusonda72@gmail.com",
    phone_number="260777371114",
    first_name="kanyanta",
    last_name="musonda",
)

print(payment_response)

reference = payment_response.get('reference')

status = pay.verify_transaction(reference)

print(status)