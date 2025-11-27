import json
from django.shortcuts import redirect
import requests
from bookstore.settings import ip
from user_accounts.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from order.models import *
from bookstore.settings import ip
from .utils import payment_received
from bookstore.settings import API_KEY

def initkhalti(request,amount,order_id,customer_id):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = f'{ip}payment/api/verify-khalti/'
    website_url = ip
    amount = amount * 100 # khalti takes in paisa
    purchase_order_id = order_id
    user = CustomUser.objects.get(uuid=customer_id)
    


    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": str(purchase_order_id),
        "purchase_order_name": "book",
        "customer_info": {
        "name": user.full_name,
        "email": user.email,
        "phone": user.phone
        }
    })

    # put your own live secet for admin
    headers = {
        'Authorization': f'key {API_KEY}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("""""""""""""""""""""""""""""")
    try:
        new_res = json.loads(response.text)
        return new_res
        
    except:
        return Response({'error': 'Validation Error'}, status=status.HTTP_400_BAD_REQUEST)

    

    
   



class VerifyKhalti(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Endpoint URL for Khalti payment verification
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        
        # Headers required for the API request
        headers = {
            'Authorization': f'key {API_KEY}',
            'Content-Type': 'application/json',
        }
        try:

        # Extracting 'pidx' from the request data
                pidx = request.query_params.get('pidx')
                purchase_order_id = request.query_params.get('purchase_order_id')
                order = Orders.objects.get(uuid=purchase_order_id)
                payment_detail = PaymentDetail.objects.get(order_id=purchase_order_id)
                print(payment_detail)

                print(pidx)
                
                # Creating the request data in JSON format
                data = json.dumps({
                    'pidx': pidx
                })
                
                # Sending a POST request to Khalti API
                response = requests.post(url, headers=headers, data=data)
                
                
                # Parsing the response
                if response.status_code == 200:
                    response_data = response.json()
                    print(response_data)
                    payment_detail.status = response_data.get('status')
                    payment_detail.transaction_id = response_data.get('transaction_id')
                    payment_detail.details = response_data
                    payment_detail.save()
                    if response_data.get('status') == 'Completed':
                        order.is_payment_verified = True
                        order.save()
                        # Perform actions when payment is completed
                        # For example, update user's payment status in the databaseu
                        data = "Payment status completed"
                        email = order.customer.email
                        message = f"Your Payment {payment_detail.amount} is Received."
                        # payment_received(message,email,order)
                        current_url = f"https://www.destinybookshub.com//?payment_status={data}" 
                        return redirect(current_url)
                    else:
                        # Payment status is not completed
                        data = "Payment status not completed"
                        current_url = f"https://www.destinybookshub.com/?payment_status={data}" 
                        return redirect(current_url)
                else:
                    # Error occurred while communicating with Khalti API
                    data = "Failed to verify payment"
                    current_url = f"https://www.destinybookshub.com/?payment_status={data}" 
                    return redirect(current_url)
                
        except:
            data = "Your Payment Request is not Completed"
            current_url = f"https://www.destinybookshub.com/?payment_status={data}" 
            return redirect(current_url)
        
            
            