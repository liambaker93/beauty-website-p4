from django import forms
from .models import InformationRequest


class ContactForm(forms.ModelForm):
    """
    The contact form
    """
    class Meta:
        model = InformationRequest
        fields = ('name', 'email', 'message')
