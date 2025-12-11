
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import FeedbackForm
from .models import Feedback
import threading
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
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [feedback.email]

    # Render HTML email
    html_content = render_to_string('feedback/email_template.html', {
        'name': feedback.name
    })

    # Send asynchronously
    send_email_async(subject, html_content, from_email, to_email)
