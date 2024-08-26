import requests
import xml.etree.ElementTree as ET

class DPOPayment:    
    company_token = ''
    
    def create_token(payment_amount, company_ref, description, service_date, ptl=5):
        trns_url = 'https://secure.3gdirectpay.com/API/v6/'
        redirect_url = f"http://127.0.0.1:8000/cart/success/{company_ref}" # company_ref will be transaction_id
        payment_currency = 'ZMW'
        service_type = 45
        service_description = f"payment for {description} from zedmarket.net"
        # the description will be obtained from product title
        # service_date will be obtained from product date

        # Create the XML request
        xml_request = f'''<?xml version="1.0" encoding="utf-8"?>
        <API3G>
            <CompanyToken>{DPOPayment.company_token}</CompanyToken>
            <Request>createToken</Request>
            <Transaction>
                <PaymentAmount>{payment_amount}</PaymentAmount>
                <PaymentCurrency>{payment_currency}</PaymentCurrency>
                <CompanyRef>{company_ref}</CompanyRef>
                <RedirectURL>{redirect_url}</RedirectURL>
                <CompanyRefUnique>0</CompanyRefUnique>
                <PTL>{ptl}</PTL>
            </Transaction>
            <Services>
                <Service>
                    <ServiceType>{service_type}</ServiceType>
                    <ServiceDescription>{service_description}</ServiceDescription>
                    <ServiceDate>{service_date}</ServiceDate>
                </Service>
            </Services>
        </API3G>'''
        
        headers = {'Content-Type': 'application/xml'}
        
        # Send the request to DPO
        response = requests.post(trns_url, data=xml_request, headers=headers)
        
        # Parse the XML response
        root = ET.fromstring(response.content)
        result = root.find('Result').text
        explanation = root.find('ResultExplanation').text
        token = root.find('TransToken').text if root.find('TransToken') is not None else None
        
        return {
            'result': result,
            'explanation': explanation,
            'token': token
        }
    
    def verify_token(transaction_token):
        vrfy_url = f'https://secure.3gdirectpay.com/payv2.php?ID={transaction_token}'
        # Create the XML request for verification
        xml_request = f'''<?xml version="1.0" encoding="utf-8"?>
        <API3G>
            <CompanyToken>{DPOPayment.company_token}</CompanyToken>
            <Request>verifyToken</Request>
            <TransactionToken>{transaction_token}</TransactionToken>
        </API3G>'''
        
        headers = {'Content-Type': 'application/xml'}
        
        # Send the verification request to DPO
        response = requests.post(vrfy_url, data=xml_request, headers=headers)
        
        # Parse the XML response
        root = ET.fromstring(response.content)
        result = root.find('Result').text
        explanation = root.find('ResultExplanation').text
        
        # You can extract more fields from the response as needed
        transaction_data = {
            'result': result,
            'explanation': explanation,
            'customer_name': root.find('CustomerName').text if root.find('CustomerName') is not None else None,
            'transaction_amount': root.find('TransactionAmount').text if root.find('TransactionAmount') is not None else None,
            # Add more fields as needed
        }
        
        return transaction_data
