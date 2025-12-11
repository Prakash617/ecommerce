from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'feedback']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'तपाईंको नाम',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'तपाईंको इमेल',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'तपाईंको फोन नम्बर',
                'required': True
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'तपाईंको प्रतिक्रिया',
                'rows': 5,
                'required': True
            }),
        }
        labels = {
            'name': 'नाम',
            'email': 'इमेल',
            'phone': 'फोन नम्बर',
            'feedback': 'प्रतिक्रिया'
        }

