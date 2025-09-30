from django import forms
from .models import Appointments


class BookingForm(forms.ModelForm):
    """
    A form used for users to book appointments
    """
