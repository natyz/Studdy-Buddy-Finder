from django import forms
from .models import EmailMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = EmailMessage
        fields = ["name", "email", "message"]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Enter your name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
        }