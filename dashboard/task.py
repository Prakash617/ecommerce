

from celery import shared_task
from django.core.mail import send_mail
from dashboard.models import NewsletterEmail
from website.models import Newsletter


@shared_task
def send_newsletter_email(topic, content):
    # Fetch subscribers' email addresses from the database
    subscribers = Newsletter.objects.filter(opt_out=False)
    # Send email to each subscriber
    for subscriber in subscribers:
        send_mail(
            topic,
            content,
            'newsletter@example.com',  # Sender's email address
            [subscriber],
            fail_silently=False,
        )
