
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import FeedbackForm
from .models import Feedback
import threading
import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            
            # Send thank you email
            send_thank_you_email(feedback)
            
            messages.success(request, 'धन्यवाद! तपाईंको प्रतिक्रिया सफलतापूर्वक पेश गरियो।')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/form.html', {'form': form})


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
        thread = threading.Thread(
            target=send_sms_async,
            args=(phone_number, message, sms_api),
            daemon=True  # Thread won't prevent system shutdown
        )
        thread.start()
        return True  # Immediately return without waiting
    except Exception as e:
        print(f"Error starting SMS thread: {e}")
        return False


def send_email_async(subject, html_content, from_email, to_email):
    """Runs the email sending in a separate thread."""
    def _send():
        email = EmailMultiAlternatives(subject, '', from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()

    thread = threading.Thread(target=_send)
    thread.start()


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
    link = 'https://drive.google.com/file/d/1Warj13mHzeC_LoILGVsmgeaIhf4DfQe0/view'
    sms_message = f'नमस्कार {feedback.name} ज्यू, यस संस्थाको १६ औं वार्षिक साधारण सभामा उपस्थित हुनुभएकोमा हार्दिक स्वागत गर्दछौं। संस्थाको १६ औं वार्षिक प्रतिवेदनको लागि यो लिंकमा जानुहोला। {link}'
    send_sms(feedback.phone, sms_message)



