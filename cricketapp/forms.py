from django import forms
from .models import ContactMessage
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

