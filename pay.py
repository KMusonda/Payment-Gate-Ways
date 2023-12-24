from paypesapal import PayWithPayPesapal
import time

# Create an instance of PayWithPayPesapal
pay_with_pesapal = PayWithPayPesapal()

# Call the paysapal_payment_request function with the required arguments
payment_response = pay_with_pesapal.paysapal_payment_request(
    amount=100,
    email_address="kanyantamusonda72@gmail.com",
    phone_number="260777371114",
    first_name="kanyanta",
    last_name="musonda"
)

# Print or use the payment response including redirect_url
print(payment_response)
print("Redirect URL:", payment_response.get("order_tracking_id"))

# Assuming you use the redirect URL to complete the payment, simulate a delay before checking the payment status
time.sleep(5)  # Adjust this delay as needed

# Get payment status using the redirect URL obtained earlier
if payment_response.get("order_tracking_id"):
    payment_status = pay_with_pesapal.get_transaction_status(payment_response.get("order_tracking_id"))
    print("Payment Status:", payment_status)
else:
    print("No redirect URL found to check payment status.")

