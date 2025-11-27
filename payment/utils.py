from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from bookstore.settings import ip

# def order_received(message, email,order):
#     message = message 
#     order = order
#     subject, from_email, to = 'Order Received!!!', 'from@test.com', email
#     html_content = render_to_string('billing/order_received.html', {'message':message,'order':order}) 
#     text_content = strip_tags(html_content) 

#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

def payment_received(message, email,order):
    logo_url = f'{ip}static/img/logo/logo.png'
    message = message 
    order = order
    subject, from_email, to = 'Payment Received!!!', 'from@test.com', email
    html_content = render_to_string('billing/payment_received.html', {'message':message,'order':order,'logo_url':logo_url}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_order_email(email, order_data):
    logo_url = f'{ip}static/img/logo/logo.png'
    subject, from_email, to = 'Your Order Has Been Placed', "from@gmail.com", email
    html_content = render_to_string('emails/order_email.html', {"order": order_data,'logo_url':logo_url}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()