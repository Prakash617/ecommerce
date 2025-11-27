from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verify_email(link, email,username):
    verify_link = link 
    subject, from_email, to = 'Verify Your Email', 'from@test.com', email
    html_content = render_to_string('verify_email.html', {'link':verify_link,'username':username}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_resetpassword_link(link, email):
    verify_link = link 
    subject, from_email, to = 'Reset Password Notification', 'from@test.com', email
    html_content = render_to_string('reset_passwordlink.html', {'link':verify_link}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()