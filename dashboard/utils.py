from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verify_email(topic, email,content):
    topic = topic 
    subject, from_email, to = 'Verify Your Email', 'from@test.com', email
    html_content = render_to_string('newsletter/newsletter.html', {'topic':topic,'content':content}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()