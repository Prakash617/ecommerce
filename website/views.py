# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import FeedbackForm
from .models import Feedback
import threading
import requests
from django.db.models import Count
from django.db.models.functions import TruncDate

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            
            # Send thank you email and SMS
            send_thank_you_email(feedback)
            
            # Redirect to success page instead of showing message
            return redirect('feedback_success', pk=feedback.pk)
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/form.html', {'form': form})


def feedback_success_view(request, pk):
    """Display success page after form submission"""
    try:
        feedback = Feedback.objects.get(pk=pk)
        return render(request, 'feedback/success.html', {'feedback': feedback})
    except Feedback.DoesNotExist:
        return redirect('feedback')


def send_sms_async(phone_number: str, message: str, sms_api: str):
    try:
        request_url = "https://sms.aakashsms.com/sms/v3/send"
        payload = {
            "auth_token": sms_api,
            "to": phone_number,
            "text": message
        }
        response = requests.post(request_url, json=payload)
        print(f"[SMS THREAD] Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[SMS THREAD] Error sending SMS: {e}")
        

def send_sms(phone_number: str, message: str) -> bool:
    try:
        sms_api = "a5c721be4a76bf54964b12641e02a1d680db8f20dfc29aaf2d3a34e05cd2901c"
        send_sms_async(phone_number, message, sms_api)
        return True
    except Exception as e:
        print(f"Error starting SMS thread: {e}")
        return False


def send_email_async(subject, html_content, from_email, to_email):
    """Runs the email sending in a separate thread."""
    def _send():
        email = EmailMultiAlternatives(subject, '', from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
    _send()


def send_thank_you_email(feedback):
    subject = 'धन्यवाद - Zest Ideology Saving & Credit Co-operative Ltd.'
    from_email = 'Zest Ideology <noreply.zestideologycoop@gmail.com>'
    to_email = [feedback.email]

    # Render HTML email
    html_content = render_to_string('feedback/email_template.html', {
        'name': feedback.name
    })

    # Send asynchronously
    send_email_async(subject, html_content, from_email, to_email)
    
    # Send SMS
    link = 'https://drive.google.com/file/d/1Warj13mHzeC_LoILGVsmgeaIhf4DfQe0/view'
    sms_message = f'नमस्कार {feedback.name} ज्यू, यस संस्थाको १६ औं वार्षिक साधारण सभामा उपस्थित हुनुभएकोमा हार्दिक स्वागत गर्दछौं। संस्थाको १६ औं वार्षिक प्रतिवेदनको लागि यो लिंकमा जानुहोला। {link}'
    send_sms(feedback.phone, sms_message)

def feedback_list_view(request):
    """Display all registered users with statistics"""
    # Get all feedbacks ordered by most recent
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    # Total count
    total_count = feedbacks.count()
    
    # Count with email
    with_email_count = feedbacks.exclude(email__isnull=True).exclude(email='').count()
    
    # Count with feedback
    with_feedback_count = feedbacks.exclude(feedback__isnull=True).exclude(feedback='').count()
    
    # Registration by date
    registrations_by_date = feedbacks.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(count=Count('id')).order_by('-date')
    
    context = {
        'feedbacks': feedbacks,
        'total_count': total_count,
        'with_email_count': with_email_count,
        'with_feedback_count': with_feedback_count,
        'registrations_by_date': registrations_by_date,
    }
    
    return render(request, 'feedback/list.html', context)